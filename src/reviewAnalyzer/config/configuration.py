from src.reviewAnalyzer.constants import *
from src.reviewAnalyzer.utils.common import read_yaml, create_directories
from src.reviewAnalyzer.entity.config_entity import (DataIngestionConfig,
                                                 DataTransformationConfig,
                                                 DataAnalysisConfig)


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            pages=config.pages,
            page_size=config.page_size
        )

        return data_ingestion_config
    

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            source_data_path=config.source_data_path,
            local_data_path=config.local_data_path,
            feature_for_new_feature=config.feature_for_new_feature,
            feature_split_string=config.feature_split_string,
            new_feature=config.new_feature
        )

        return data_transformation_config


    def get_data_analysis_config(self) -> DataAnalysisConfig:
        config = self.config.data_analysis
        create_directories([config.root_dir])

        data_analysis_config = DataAnalysisConfig(
            root_dir=config.root_dir,
            source_data_path=config.source_data_path
        )

        return data_analysis_config
    