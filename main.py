import sys
from src.reviewAnalyzer import logger
from src.reviewAnalyzer.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from src.reviewAnalyzer.pipeline.stage_02_data_transformation import DataTransformationPipeline
from src.reviewAnalyzer.pipeline.stage_03_data_analysis import DataAnalysisPipeline
from src.reviewAnalyzer.exceptions import CustomException


STAGE_NAME = "Data Ingestion stage"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
   data_ingestion = DataIngestionPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<]\n[x==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e, sys)


STAGE_NAME = "Data Transformation Stage"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
   data_transformation = DataTransformationPipeline()
   data_transformation.main()
   logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<]\n[x==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e, sys)


STAGE_NAME = "Data Analysis Stage"
try: 
   logger.info(f"*******************")
   logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
   data_analysis = DataAnalysisPipeline()
   data_analysis.main()
   logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<]\n\n[x==========x")
except Exception as e:
    logger.exception(e)
    raise CustomException(e, sys)
