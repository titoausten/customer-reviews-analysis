from src.reviewAnalyzer.config.configuration import ConfigurationManager
from src.reviewAnalyzer.components.data_transformation import DataTransformation
from src.reviewAnalyzer.utils.common import get_size
from src.reviewAnalyzer import logger
from pathlib import Path
import os
import sys
from src.reviewAnalyzer.exceptions import CustomException


STAGE_NAME = "Data Transformation stage"


class DataTransformationPipeline:
    def __init__(self):
        pass

    def main(self):  
        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()

        if not os.path.exists(data_transformation_config.local_data_path):
            data_transformation = DataTransformation(config=data_transformation_config)
            new_data = data_transformation.create_feature()
            print(f"Cleaning data file...")
            new_data['cleaned_reviews'] = new_data['reviews'].apply(data_transformation.clean_data)
            logger.info(f"Data file cleaned")
            logger.info(f"Part of Speech Tagging...")
            print(f"Tokenizing...")
            print(f"Part of Speech Tagging...")
            print(f"Removing stopwords...")
            new_data['pos_tagged'] = new_data['cleaned_reviews'].apply(data_transformation.process_data)
            logger.info(f"Part of Speech Tagging done.")
            print(f"Word lemmatizing...")
            new_data['corpus'] = new_data['pos_tagged'].apply(data_transformation.lemmatiza)
            logger.info(f"Word lemmatizing done and corpus feature created.")
            data_transformation.save_data(new_data)
        else:
            logger.info(f"File already exists of size: {get_size(Path(data_transformation_config.local_data_path))}")


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        data_transformation = DataTransformationPipeline()
        data_transformation.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<]\n[x==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e, sys)
