import os
import io
import pickle
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from src.constants import GOGGLE_KEY_PATH, GOOGLE_FOLDER_ID, MODEL_FILE_NAME
from src.exception import MyException
from src.logger import logging

class GoogleDriveModelManager:
    def __init__(self, key_path:str = GOGGLE_KEY_PATH, folder_id:str = GOOGLE_FOLDER_ID):
        self.key_path = key_path
        self.folder_id = folder_id
        self.service = self._authenticate()

    def _authenticate(self):
        try:
            scopes = ['https://www.googleapis.com/auth/drive']
            creds = service_account.Credentials.from_service_account_file(
                self.key_path, scopes=scopes)
            return build('drive', 'v3', credentials=creds)
        except Exception as e:
            logging.error('Something went wrong while connecting to cloud : %s',e)
            raise MyException(e, sys) from e

    def upload_model(self, local_path: str, drive_filename: str = MODEL_FILE_NAME) -> str:
        file_metadata = {'name': drive_filename, 'parents': [self.folder_id]}
        media = MediaFileUpload(local_path, mimetype='application/octet-stream')

        file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        
        print(f"Uploaded '{drive_filename}' successfully. File ID: {file.get('id')}")
        return file.get('id')

    def download_model(self, drive_filename: str = MODEL_FILE_NAME):
        """
        Downloads the model file from Google Drive and loads it into memory using pickle.
        Returns the loaded model object.
        """
        file_id = self._get_file_id(drive_filename)
        if not file_id:
            print(f"File '{drive_filename}' not found in Drive folder.")
            return None

        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

        fh.seek(0)
        model = pickle.load(fh)
        print(f"Model '{drive_filename}' loaded from Google Drive into memory.")
        return model

    def delete_model(self, drive_filename: str = MODEL_FILE_NAME):
        file_id = self._get_file_id(drive_filename)
        if not file_id:
            print(f"File '{drive_filename}' not found for deletion.")
            return False

        self.service.files().delete(fileId=file_id).execute()
        print(f"Deleted '{drive_filename}' successfully.")
        return True

    def file_exists(self, drive_filename: str = MODEL_FILE_NAME) -> bool:
        file_id = self._get_file_id(drive_filename)
        exists = file_id is not None
        print(f"File '{drive_filename}' exists: {exists}")
        return exists

    def _get_file_id(self, filename: str):
        query = f"name='{filename}' and '{self.folder_id}' in parents and trashed=false"
        results = self.service.files().list(q=query, fields='files(id, name)').execute()
        items = results.get('files', [])
        return items[0]['id'] if items else None
        
        
if __name__=='__main__':
    con = GoogleDriveModelManager()
    con.upload_model(local_path=r'C:\Users\idipa\OneDrive\Desktop\MLOPS\Vehicle-Insurance-Domain\artifact\05_27_2025_22_27_02\model_trainer\trained_model\model.pkl')
    print("Uploaded successfull")
    print("File exists : ",con.file_exists())
    model = con.download_model()
    print(model)
    print("model downloaded")
    print("Model deleted : ",con.delete_model())
    print("File exists : ",con.file_exists())

