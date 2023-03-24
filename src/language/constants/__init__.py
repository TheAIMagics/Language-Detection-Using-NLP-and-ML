import os

ARTIFACTS_DIR: str = "artifacts"

# constants related to data ingestion
DATA_INGESTION_ARTIFACTS_DIR: str = "data_ingestion"
S3_BUCKET_DATA_URI = "s3://lang-detection/data/"
S3_DATA_FILE_NAME: str = "lang_detection.csv"
DATA_DIR_NAME: str = "data"

# constants related to data tranformation
DATA_TRANSFORMATION_ARTIFACTS_DIR: str = "data_transformation"
TRANSFORM_OBJECT_NAME :str = 'transform.pkl'
ENCODER_NAME : str = 'encoder.pkl'
X_DIR_NAME :str = 'X'
y_DIR_NAME: str = 'y'

# constants related to model training
MODEL_TRAINER_ARTIFACTS_DIR : str = 'model_training'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")


# constants related to Model Evauation
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
S3_BUCKET_MODEL_URI: str = "s3://lang-detection/model"
MODEL_EVALUATION_DIR: str = "model_evaluation"
S3_MODEL_DIR_NAME: str = "s3_model"
S3_MODEL_NAME: str = "model.pkl"
MODEL_NAME: str = "model.pkl"