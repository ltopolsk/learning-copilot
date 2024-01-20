from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
from gridfs import GridFS

# config = json.load(open("config.json"))



class DBClient:

    def __init__(self, config):
        self.client = MongoClient(config['uri'])
        self.db = self.client['ZPDS-database']
        self.fs = GridFS(self.db)

    def get_db(self):
        return self.db

    def upload_notes(self, id, pdf_content, filename):
        collection = self.db[id]['notes']
        self.upload_pdf(collection, pdf_content, filename)
    
    def upload_quiz(self, id, pdf_content, filename):
        collection = self.db[id]['quizes']
        self.upload_pdf(collection, pdf_content, filename)

    def upload_pdf(self, collection, pdf_content, filename):
        file_id = self.fs.put(pdf_content, filename=filename)
        metadata = {
            'filename': filename,
            'file_id': file_id
        }
        collection.insert_one(metadata)
    
    def get_notes(self, id):
        collection = self.db[id]['notes']
        return collection.find({})
