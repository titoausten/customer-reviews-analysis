from src.reviewAnalyzer import logger
from src.reviewAnalyzer.utils.common import *
from src.reviewAnalyzer.entity.config_entity import DataAnalysisConfig
from pathlib import Path
from src.reviewAnalyzer.config.configuration import ConfigurationManager
from src.reviewAnalyzer.components.data_analysis import DataAnalysis
import os
import sys
from src.reviewAnalyzer.exceptions import CustomException


STAGE_NAME = "Data Analysis stage"


class DataAnalysisPipeline:
    def __init__(self):
        pass

    def main(self):  
        config = ConfigurationManager()
        data_transformation_config = config.get_data_analysis_config()
        
        data_analysis = DataAnalysis(config=data_transformation_config)
        data = load_data(data_transformation_config.source_data_path)
        data = data.reset_index(drop=True)

        # Sentiment Analysis using VADER
        data['sentiment'] = data['corpus'].apply(data_analysis.sentiment_analysis)
        data['analysis'] = data['sentiment'].apply(data_analysis.vader_analysis)

        title = 'Review Sentiment Chart'
        plot_piechart(
            data['analysis'].value_counts(),
            Path(data_transformation_config.root_dir+'/'+title+'.png'),
            title
            )
        logger.info(f"Sentiment analysis calculated")
        logger.info(f"{title} saved at {data_transformation_config.root_dir+'/'+title+'.png'}.")

        title = 'Verified Reviewer Trip Chart'
        plot_piechart(
            data['verified'].value_counts(),
            Path(data_transformation_config.root_dir+'/'+title+'.png'),
            title
            )
        logger.info(f"{title} saved at {data_transformation_config.root_dir+'/'+title+'.png'}.")

        show_wordcloud(data.corpus, Path(data_transformation_config.root_dir+'/wordcloud'+'.png'))
        logger.info(f"Wordcloud image saved at {data_transformation_config.root_dir+'/wordcloud'+'.png'}.")


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
        data_analysis = DataAnalysisPipeline()
        data_analysis.main()
        logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<]\n\n[x==========x")
    except Exception as e:
        logger.exception(e)
        raise CustomException(e, sys)
