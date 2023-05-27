import os,sys
import joblib
from src.language.constants import *
from src.language.logger import logging
from src.language.exception import CustomException
from src.language.entity.config_entity import PredictionPipelineConfig
from src.language.cloud_storage.s3_opearations import S3Sync
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from src.language.utils import *

encoder= LabelEncoder()

TF_IDF= TfidfVectorizer(ngram_range=(1,3), analyzer='char')

class SinglePrediction:
    def __init__(self):
        try:
            self.s3_sync = S3Sync()
            self.prediction_config = PredictionPipelineConfig()
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_model_in_production(self):
        try:
            s3_model_path = self.prediction_config.s3_model_path
            model_download_path = self.prediction_config.model_download_path
            os.makedirs(model_download_path, exist_ok=True)
            if len(os.listdir(model_download_path)) == 0:
                self.s3_sync.sync_folder_from_s3(folder=model_download_path, aws_bucket_url=s3_model_path)
        except Exception as e:
            raise CustomException(e, sys)

    def prediction(self, text):
        try:
            self.get_model_in_production()
            transform_obj = joblib.load(self.prediction_config.transform_file_path)
            x = transform_obj.transform([text]).toarray()
            # Load the trained model and predict the language
            model = self.prediction_config.model_file_path
            trained_model = load_object(model) 
            lang = trained_model.predict(x)
            encoder_path = self.prediction_config.encoder_file_path
            encoder = load_object(encoder_path)
            return encoder[lang]
        except Exception as e:
            raise CustomException(e, sys)

    