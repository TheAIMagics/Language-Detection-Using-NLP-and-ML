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