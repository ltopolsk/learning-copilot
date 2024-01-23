from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS


class DBClient:

    def __init__(self, config):
        self.client = MongoClient(config['uri'], server_api=ServerApi('1'))
        self.db = self.client['ZPDS-database']
        self.fs = GridFS(self.db)

    def get_db(self):
        return self.db

    def upload_notes(self, id, pdf_content, md_content, title):
        collection = self.db[id]['notes']
        metadata = {
            'title': title,
            'md_notes': md_content
        }
        self._upload_pdf(collection, pdf_content, metadata)
    
    def upload_quiz(self, id, quiz, quizname):
        collection = self.db[id]['quizes']
        collection.insert_one({'name': quizname, 'quiz': quiz})

    def _upload_pdf(self, collection, pdf_content, metadata):
        file_id = self.fs.put(pdf_content, filename=metadata['title'])
        meta = {
            **metadata,
            'file_id': file_id
        }
        collection.insert_one(meta)

    def _get_one_pdf(self, file_id):
        return self.fs.get(file_id).read()

    def get_one_notes(self, user_id, notes_id):
        metadata = self.db[user_id]['notes'].find_one({'_id': notes_id})
        return {**metadata, 'file':self._get_one_pdf(metadata['file_id'])}
    
    def get_one_quiz(self, user_id, quiz_id):
        return self.db[user_id]['quizes'].find_one({'_id': quiz_id})
    
    def get_notes(self, id):
        collection = self.db[id]['notes']
        return collection.find({})
    
    def get_quizes(self, id):
        collection = self.db[id]['quizes']
        return collection.find({})
