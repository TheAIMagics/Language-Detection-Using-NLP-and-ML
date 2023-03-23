import os,sys
from src.language.constants import *
from src.language.logger import logging
from src.language.exception import CustomException
from src.language.entity.config_entity import DataIngestionConfig
from src.language.entity.artifact_entity import DataIngestionArtifacts
from src.language.cloud_storage.s3_opearations import S3Sync

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig)-> None:

        try:
            self.data_ingestion_config = data_ingestion_config
            self.s3_sync = S3Sync()
            self.data_ingestion_artifact = self.data_ingestion_config.data_ingestion_artifact_dir
            
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_data_from_cloud(self) -> None:
        try:
            logging.info("Initiating data download from s3 bucket...")
            if os.path.exists(self.data_ingestion_config.download_dir):
                logging.info(f"Data is already available in {self.data_ingestion_config.download_dir}. Hence skipping this step")

            else:
                os.makedirs(self.data_ingestion_config.download_dir, exist_ok=True)
                print(S3_BUCKET_DATA_URI, self.data_ingestion_config.download_dir)
                self.s3_sync.sync_folder_from_s3(
                        folder=self.data_ingestion_config.download_dir, aws_bucket_url=S3_BUCKET_DATA_URI)
                logging.info(
                        f"Data is downloaded from s3 bucket to Download directory: {self.data_ingestion_config.download_dir}.")

        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        try:
            logging.info("Initiating the data ingestion component...")
            os.makedirs(self.data_ingestion_artifact,exist_ok=True)
            self.get_data_from_cloud()
            data_ingestion_artifact = DataIngestionArtifacts(
                data_folder_path=self.data_ingestion_config.download_dir
            )
            logging.info('Data ingestion is completed Successfully.')
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)