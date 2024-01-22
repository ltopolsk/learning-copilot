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

    def upload_notes(self, id, pdf_content, filename):
        collection = self.db[id]['notes']
        print(type(pdf_content))
        if type(pdf_content) == str:
            collection.insert_one({'latex_note':pdf_content,'filename':filename})
        else:
            self.upload_pdf(collection, pdf_content, filename)
    
    def upload_quiz(self, id, quiz, quizname):
        collection = self.db[id]['quizes']
        collection.insert_one({'name': quizname, 'quiz': quiz})

    def upload_pdf(self, collection, pdf_content, filename):
        file_id = self.fs.put(pdf_content, filename=filename)
        metadata = {
            'filename': filename,
            'file_id': file_id
        }
        collection.insert_one(metadata)
    
    def get_one_notes(self, user_id, notes_id):
        return self.db[user_id]['notes'].find_one({'_id': notes_id})
    
    def get_one_quiz(self, user_id, quiz_id):
        return self.db[user_id]['quizes'].find_one({'_id': quiz_id})
    
    def get_notes(self, id):
        collection = self.db[id]['notes']
        return collection.find({})
    
    def get_quizes(self, id):
        collection = self.db[id]['quizes']
        return collection.find({})
