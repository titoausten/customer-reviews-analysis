from src.reviewAnalyzer.config.configuration import ConfigurationManager
from src.reviewAnalyzer.components.data_ingestion import DataIngestion
from src.reviewAnalyzer import logger
from src.reviewAnalyzer.exceptions import CustomException
import sys


STAGE_NAME = "Data Ingestion stage"


class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion.scrape_data()


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        data_ingestion = DataIngestionPipeline()
        data_ingestion.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<]\n[x==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e, sys)
