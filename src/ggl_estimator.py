from src.cloud_storage.google_storage import GoogleDriveModelManager
from src.exception import MyException
from src.constants import GOGGLE_KEY_PATH, GOOGLE_FOLDER_ID
import sys
from pandas import DataFrame
from src.logger import logging


class GGLEstimator:
    """
    This class is used to save and retrieve our model from google drive storage and to do prediction
    """
    def __init__(self):
        try:
            self.folder_id = GOOGLE_FOLDER_ID
            self.gclient = GoogleDriveModelManager(GOGGLE_KEY_PATH,self.folder_id)
            logging.info("Connection established successful")
        except Exception as e:
            logging.error("Could not connect to the cloud")
            raise MyException(e, sys) from e
            
    def save_model(self, local_path:str, drive_filename:str):
        """
        param loacal_path: path in the local directory to the file
        param drive_filename: name of the file in the drive
        """
        try:
            status = self.gclient.upload_model(local_path=local_path,drive_filename=drive_filename)
            return True
        except Exception as e:
            raise MyException(e, sys) from e
            
    def load_model(self, drive_filename:str):
        """
        param drive_filename: name of the file in the drive
        """
        try:
            model = self.gclient.download_model(drive_filename=drive_filename)
            return model
        except Exception as e:
            raise MyException(e, sys) from e
            