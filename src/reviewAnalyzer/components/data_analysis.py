from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.reviewAnalyzer import logger
from src.reviewAnalyzer.utils.common import *
from src.reviewAnalyzer.entity.config_entity import DataAnalysisConfig
from pathlib import Path


class DataAnalysis:
    def __init__(self, config: DataAnalysisConfig):
        self.config = config
        self.file = self.config.source_data_path
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        
    # function to calculate vader sentiment
    def sentiment_analysis(self, text):
        vs = self.sentiment_analyzer.polarity_scores(text)
        return vs['compound']
    

    # function to analyse and create a new feature with sentiments
    def vader_analysis(self, compound):
        if compound >= 0.5:
            return 'Positive'
        elif compound < 0 :
            return 'Negative'
        else:
            return 'Neutral'
