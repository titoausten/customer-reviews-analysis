import os
import pandas as pd
import sys
import yaml
from src.reviewAnalyzer import logger
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import matplotlib.pyplot as plt
from src.reviewAnalyzer.exceptions import CustomException
from wordcloud import WordCloud, STOPWORDS


@ensure_annotations
def load_data(path_to_file):
    print(f"Loading source data file...")
    df = pd.read_csv(path_to_file, index_col=0)
    logger.info(f"Data file ({path_to_file}) loaded")
    return df


@ensure_annotations
def save_data_to_csv(data: pd.DataFrame, file_path):
    data.to_csv(file_path)
    logger.info(f"Preprocessed file location: {file_path}")


@ensure_annotations
def plot_piechart(values, path_to_chart: Path, chart_title: str):
    plt.figure(figsize=(10,7))
    plt.subplot(1,3,2)
    plt.title(chart_title)
    plt.pie(x=values.values, labels = values.index,
            autopct='%1.1f%%', shadow=False)
    plt.savefig(path_to_chart)


@ensure_annotations
def show_wordcloud(data, path_to_img: Path):
    wordcloud = WordCloud(
        background_color='white',
        height=600,
        width=600,
        stopwords=set(STOPWORDS),
        max_words=500,
        max_font_size=100,
        scale=3,
        random_state=1)

    wordcloud=wordcloud.generate(str(data))

    fig = plt.figure(figsize=(12, 10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig(path_to_img)


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        CustomException

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        raise CustomException(e, sys)
    


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_bin(data: Any, path: Path):
    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path): path to binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to binary file

    Returns:
        Any: object stored in the file
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"
