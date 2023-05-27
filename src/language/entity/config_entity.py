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

@dataclass
class ModelTrainingConfig:
    model_trainer_artifact_dir: str = os.path.join(from_root(), ARTIFACTS_DIR,MODEL_TRAINER_ARTIFACTS_DIR)
    trained_model_file_path: str = os.path.join(
        model_trainer_artifact_dir, MODEL_TRAINER_TRAINED_MODEL_NAME
    )
    expected_accuracy: float = MODEL_TRAINER_EXPECTED_SCORE
    model_config_file_path: str = MODEL_TRAINER_MODEL_CONFIG_FILE_PATH

@dataclass
class ModelEvaluationConfig:
    s3_model_path: str = S3_BUCKET_MODEL_URI
    model_evaluation_artifacts_dir: str = os.path.join(from_root(), ARTIFACTS_DIR, MODEL_EVALUATION_DIR)
    best_model_dir: str = os.path.join(model_evaluation_artifacts_dir, S3_MODEL_DIR_NAME)
    best_model: str = os.path.join(best_model_dir, S3_MODEL_NAME)

@dataclass
class PredictionPipelineConfig:
    s3_model_path: str = S3_BUCKET_MODEL_URI
    prediction_artifact_dir = os.path.join(from_root(), STATIC_DIR)
    model_download_path = os.path.join(prediction_artifact_dir, MODEL_SUB_DIR)
    model_file_path = os.path.join(model_download_path, MODEL_NAME)
    transform_file_path = os.path.join(model_download_path, TRANSFORM_OBJECT_NAME)
    encoder_file_path = os.path.join(model_download_path, ENCODER_NAME)