import os,sys
import numpy as np
from typing import Tuple
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf import ModelFactory
from src.language.utils import *
from src.language.entity.artifact_entity import (
    DataTransformationArtifacts,
    ClassificationMetricArtifact,
    ModelTrainerArtifact)
from src.language.entity.config_entity import ModelTrainingConfig
from src.language.constants import *
from src.language.logger import logging
from src.language.exception import CustomException

class ModelTraining:
    def __init__(self, data_transformation_artifact : DataTransformationArtifacts,
    model_trainer_config : ModelTrainingConfig):
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def get_model_object_and_report(
        self, X: np.array, y: np.array
    ) -> Tuple[object, object]:
        """
        Method Name :   get_model_object_and_report
        Description :   This function uses neuro_mf to get the best model object and report of the best model

        Output      :   Returns metric artifact object and best model object
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Using neuro_mf to get best model object and report")
            model_factory = ModelFactory(
                model_config_path=self.model_trainer_config.model_config_file_path
            )

            X_train, X_test, y_train, y_test= train_test_split(X, y, random_state=42)

            best_model_detail = model_factory.get_best_model(
                X=X_train,
                y=y_train,
                base_accuracy=self.model_trainer_config.expected_accuracy,
            )
            model_obj = best_model_detail.best_model

            y_pred = model_obj.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred,average='micro')
            precision = precision_score(y_test, y_pred,average='micro')
            recall = recall_score(y_test, y_pred,average='micro')
            metric_artifact = ClassificationMetricArtifact(
                f1_score=f1, precision_score=precision, recall_score=recall
            )

            return best_model_detail, metric_artifact

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_model_trainer(self):
        try:
            os.makedirs(self.model_trainer_config.model_trainer_artifact_dir,exist_ok=True)
            X = np.load(self.data_transformation_artifact.transformed_X_file_path)
            y = np.load(self.data_transformation_artifact.transformed_y_file_path)
            
            best_model_detail, metric_artifact =self.get_model_object_and_report(X,y)

            if (
                best_model_detail.best_score
                < self.model_trainer_config.expected_accuracy
            ):
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")
            

            X_train, X_test, y_train, y_test= train_test_split(X, y, random_state=42)
            model=best_model_detail.best_model
            model.fit(X_train, y_train)

            save_object(
                self.model_trainer_config.trained_model_file_path, model
            )
            
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact,
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
