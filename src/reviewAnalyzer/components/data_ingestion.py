import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from src.reviewAnalyzer import logger
from src.reviewAnalyzer.utils.common import get_size
from src.reviewAnalyzer.entity.config_entity import DataIngestionConfig
from pathlib import Path


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    
    def scrape_data(self):
        if not os.path.exists(self.config.local_data_file):
            reviews = []

            for i in range(1, self.config.pages + 1):

                print(f"Scraping page {i}")

                # Create URL to collect links from paginated data
                url = f"{self.config.source_URL}/page/{i}/?sortby=post_date%3ADesc&pagesize={self.config.page_size}"

                # Collect HTML data from this page
                response = requests.get(url)

                # Parse content
                content = response.content
                parsed_content = BeautifulSoup(content, 'html.parser')
                for para in parsed_content.find_all("div", {"class": "text_content"}):
                    reviews.append(para.get_text())
            
                print(f"   ---> {len(reviews)} total reviews")
            logger.info("Scraping complete!")

            # Load scraped data into a dataframe
            df = pd.DataFrame()
            df["reviews"] = reviews

            # Save to csv file
            df.to_csv(self.config.local_data_file)

            logger.info(f"Scraped File location: {self.config.local_data_file}")
            
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
