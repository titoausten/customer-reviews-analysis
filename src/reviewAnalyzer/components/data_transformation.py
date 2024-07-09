from src.reviewAnalyzer import logger
from src.reviewAnalyzer.utils.common import get_size
from src.reviewAnalyzer.entity.config_entity import DataTransformationConfig
from pathlib import Path

import os
import re
import pandas as pd
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.file = self.config.source_data_path
        self.lemmatizer = WordNetLemmatizer()
        self.df = self.load_data()

    
    def load_data(self):
        # Load data
        print(f"Loading source data file...")
        df = pd.read_csv(self.file, index_col=0)
        logger.info(f"Data file ({self.file}) loaded")
        return df
        

    def create_feature(self):      
        # df = self.load_data()
        # Create a column in the dataframe based on what another feature contains
        print(f"Creating feature ({self.config.new_feature}) from ({self.config.feature_for_new_feature})")
        self.df[self.config.new_feature] = self.df[self.config.feature_for_new_feature].str.contains(self.config.feature_split_string)
        logger.info(f"Feature ({self.config.new_feature}) created")
        return self.df
        

    def clean_data(self, document):
        # df = self.create_feature()
        document = document.split('|')[1]
        document = re.sub('[^a-zA-Z]',' ', str(document))
        document = document.lower()
        document = document.split()
        # Fixing contractions e.g don't, won't etc.
        #document = contractions.fix(document)
        document = " ".join(document)
        return document
    

    def process_data(self, document):
        tokens = word_tokenize(document)
        tagged_tokens = pos_tag(tokens)
        tag_map = {'J':wordnet.ADJ, 'V':wordnet.VERB, 'N':wordnet.NOUN, 'R':wordnet.ADV}
        new_tagged_tokens = []
        for word, tag in tagged_tokens:
            if word.lower() not in set(stopwords.words('english')):
                new_tagged_tokens.append(tuple([word, tag_map.get(tag[0])]))
        return new_tagged_tokens


    def lemmatiza(self, document):
        #df = self.process_data()
        lemmatized_text = " "
        for word, tag in document:
            if not tag:
                lemmatize = word
                lemmatized_text = lemmatized_text + " " + lemmatize
            else:
                lemmatize = self.lemmatizer.lemmatize(word, pos=tag)
                lemmatized_text = lemmatized_text + " " + lemmatize
        return lemmatized_text


    def save_data(self, document: pd.DataFrame):
        document.to_csv(self.config.local_data_path)
        logger.info(f"Preprocessed file location: {self.config.local_data_path}")
