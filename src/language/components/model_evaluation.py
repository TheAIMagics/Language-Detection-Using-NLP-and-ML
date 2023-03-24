import os,sys
import numpy as np
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.language.constants import *
from src.language.utils import *
from src.language.logger import logging
from src.language.exception import CustomException
from src.language.cloud_storage.s3_opearations import S3Sync
from src.language.entity.config_entity import ModelEvaluationConfig
from src.language.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifacts,ModelEvaluationArtifact

@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float


class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig, 
    data_transformation_artifact=DataTransformationArtifacts,
    model_trainer_artifact= ModelTrainerArtifact) -> None:
        self.model_evaluation_config = model_evaluation_config
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact

    def get_best_model(self):
        try:
            model_path = self.model_evaluation_config.s3_model_path
            best_model_dir = self.model_evaluation_config.best_model_dir
            os.makedirs(os.path.dirname(best_model_dir), exist_ok=True)
            s3_sync = S3Sync()
            best_model_path = None
            s3_sync.sync_folder_from_s3(
                folder=best_model_dir, aws_bucket_url=model_path)
            for file in os.listdir(best_model_dir):
                if file.endswith(".pt"):
                    best_model_path = os.path.join(best_model_dir, file)
                    logging.info(f"Best model found in {best_model_path}")
                    break
                else:
                    logging.info("Model is not available in best_model_directory")

            return best_model_path

        except Exception as e:
            raise CustomException(e, sys)
        
    def evaluate_model(self) -> EvaluateModelResponse:
        try:
            X = np.load(self.data_transformation_artifact.transformed_X_file_path)
            y = np.load(self.data_transformation_artifact.transformed_y_file_path)
            X_train, X_test, y_train, y_test= train_test_split(X, y, random_state=42)

            trained_model = load_object(
                file_path=self.model_trainer_artifact.trained_model_file_path
            )
            trained_model_f1_score = (
                self.model_trainer_artifact.metric_artifact.f1_score
            )
            best_model_f1_score = None
            best_model = self.get_best_model()
            
            if best_model is not None:
                y_hat_best_model = best_model.predict(X_test)
                best_model_f1_score = f1_score(y_test, y_hat_best_model)

            # calucate how much percentage training model accuracy is increased/decreased
            tmp_best_model_score = (
                0 if best_model_f1_score is None else best_model_f1_score
            )
            result = EvaluateModelResponse(
                trained_model_f1_score=trained_model_f1_score,
                best_model_f1_score=best_model_f1_score,
                is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                difference=trained_model_f1_score - tmp_best_model_score,
            )
            logging.info(f"Result: {result}")
            return result
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        """
        Method Name :   initiate_model_evaluation
        Description :   This function is used to initiate all steps of the model evaluation

        Output      :   Returns model evaluation artifact
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Initiating the data Transformation component...")
            evaluate_model_response = self.evaluate_model()

            s3_model_path = self.model_evaluation_config.s3_model_path

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=evaluate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference,
            )

            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            logging.info("Completed  Model Evaluation component...")
            return model_evaluation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
