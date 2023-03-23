import os, sys
from dataclasses import dataclass
from from_root import from_root
from src.language.constants import *

@dataclass
class DataIngestionConfig:
    data_ingestion_artifact_dir: str = os.path.join(from_root(), ARTIFACTS_DIR,DATA_INGESTION_ARTIFACTS_DIR)
    download_dir = os.path.join(data_ingestion_artifact_dir,DATA_DIR_NAME)
    data_path : str = os.path.join(download_dir, S3_DATA_FILE_NAME)