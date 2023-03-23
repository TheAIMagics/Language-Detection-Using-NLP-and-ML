import os,sys
import re
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from src.language.utils import *
from src.language.constants import *
from src.language.logger import logging
from src.language.exception import CustomException
from src.language.entity.config_entity import DataTransformationConfig
from src.language.entity.artifact_entity import DataTransformationArtifacts, DataIngestionArtifacts
from src.language.cloud_storage.s3_opearations import S3Sync

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,
     data_ingestion_artifact: DataIngestionArtifacts)-> None:
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self)-> DataTransformationArtifacts:
        try:
            logging.info("Initiating the data Transformation component...")
            os.makedirs(self.data_transformation_config.data_transformation_artifact_dir,exist_ok=True)

            csv_path = os.path.join(self.data_ingestion_artifact.data_folder_path,"lang_detection.csv")
            df = pd.read_csv(csv_path)
            # There are 66 duplicate rows, SO we will drop them 
            df.drop(df[df.duplicated()].index, axis=0, inplace=True)
            # Create copy of dataframe
            df_copy= df.copy()
            df_copy['cleaned_Text']= ""

            # Text preprocessing on df_copy
            def clean_function(Text):
                # removing the symbols and numbers
                Text = re.sub(r'[\([{})\]!@#$,"%^*?:;~`0-9]', ' ', Text)
                
                # converting the text to lower case
                Text = Text.lower()
                Text = re.sub('http\S+\s*', ' ', Text)  # remove URLs
                Text = re.sub('RT|cc', ' ', Text)  # remove RT and cc
                Text = re.sub('#\S+', '', Text)  # remove hashtags
                Text = re.sub('@\S+', '  ', Text)  # remove mentions
                Text = re.sub('\s+', ' ', Text)  # remove extra whitespace
                
                return Text
            
            df_copy['cleaned_Text'] = df_copy['Text'].apply(lambda x: clean_function(x))
            # Separating Independent and Dependent Features
            X= df_copy["cleaned_Text"]
            y= df_copy["Language"]

            encoder= LabelEncoder()
            y_array= encoder.fit_transform(y)

            # Apply VEctoriztion technique TFIDF
            TF_IDF = TfidfVectorizer(ngram_range=(1,3), analyzer='char')
            X_array = TF_IDF.fit_transform(X).toarray()
            joblib.dump(TF_IDF,self.data_transformation_config.transformer_object_path)
            joblib.dump(encoder,self.data_transformation_config.encoder_file_path)
            
            # Saving X and y numpy arrays
            os.makedirs(self.data_transformation_config.X_array_path,exist_ok=True)
            X_file_path = os.path.join(self.data_transformation_config.X_array_path,'X.npy')
            np.save(X_file_path,X_array)
            os.makedirs(self.data_transformation_config.y_array_path,exist_ok=True)
            y_file_path = os.path.join(self.data_transformation_config.y_array_path,'y.npy')
            np.save(y_file_path,y_array)
            logging.info('Data Transformation is completed Successfully.')

            data_transformation_artifact = DataTransformationArtifacts(
                transformed_X_file_path=X_file_path,
                transformed_y_file_path=y_file_path
                )
            
            logging.info('Data Transformation is completed Successfully.')
            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys)