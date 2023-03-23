import os, sys
from dataclasses import dataclass
from from_root import from_root
from src.language.constants import *

@dataclass
class DataIngestionConfig:
    data_ingestion_artifact_dir: str = os.path.join(from_root(), ARTIFACTS_DIR,DATA_INGESTION_ARTIFACTS_DIR)
    download_dir = os.path.join(data_ingestion_artifact_dir,DATA_DIR_NAME)
    data_path : str = os.path.join(download_dir, S3_DATA_FILE_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_artifact_dir: str = os.path.join(from_root(), ARTIFACTS_DIR,DATA_TRANSFORMATION_ARTIFACTS_DIR)
    X_array_path : str = os.path.join(data_transformation_artifact_dir,X_DIR_NAME)
    y_array_path : str = os.path.join(data_transformation_artifact_dir,y_DIR_NAME)
    transformer_object_path: str = os.path.join(data_transformation_artifact_dir, TRANSFORM_OBJECT_NAME)
    encoder_file_path = os.path.join(data_transformation_artifact_dir, ENCODER_NAME)