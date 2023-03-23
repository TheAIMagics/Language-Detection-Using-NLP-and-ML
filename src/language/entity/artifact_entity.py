from dataclasses import dataclass

# Data ingestion artifacts
@dataclass
class DataIngestionArtifacts:
    data_folder_path: str

# Data transformation artifacts
@dataclass
class DataTransformationArtifacts:
    transformed_X_file_path : str
    transformed_y_file_path : str
