from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path
    pages: int
    page_size: int


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    source_data_path: str
    local_data_path: Path
    feature_for_new_feature: str
    feature_split_string: str
    new_feature: str


@dataclass(frozen=True)
class DataAnalysisConfig:
    root_dir: Path
    source_data_path: str
