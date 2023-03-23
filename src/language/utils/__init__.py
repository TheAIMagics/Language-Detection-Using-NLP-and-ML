import os,sys
import dill
import numpy as np
from src.language.logger import logging
from src.language.exception import CustomException

def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of MainUtils class")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

        logging.info("Exited the save_object method of MainUtils class")

    except Exception as e:
        raise CustomException(e, sys) from e
    
def load_object(file_path: str) -> object:
    logging.info("Entered the load_object method of MainUtils class")

    try:

        with open(file_path, "rb") as file_obj:
            obj = dill.load(file_obj)

        logging.info("Exited the load_object method of MainUtils class")

        return obj

    except Exception as e:
        raise CustomException(e, sys) from e