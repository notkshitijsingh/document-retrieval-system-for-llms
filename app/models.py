import sqlite3
from .utils import encode_text
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class DocumentModel:
    @staticmethod
    def add_document(text):
        """Adds a document to the database."""
        conn = sqlite3.connect('data/documents.db')
        cursor = conn.cursor()

        # Encode the document text
        embedding = encode_text(text).tobytes()

        # Insert document into the database
        cursor.execute('INSERT INTO documents (text, embedding) VALUES (?, ?)', (text, embedding))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_documents():
        conn = sqlite3.connect('data/documents.db')
        cursor = conn.cursor()
        cursor.execute('SELECT text, embedding FROM documents')
        documents = cursor.fetchall()
        conn.close()

        # Decode embeddings
        return [{"text": doc[0], "embedding": np.frombuffer(doc[1], dtype=np.float32)} for doc in documents]

    @staticmethod
    def calculate_similarity(query_vector, doc_vector):
        return cosine_similarity([query_vector], [doc_vector])[0][0]



class UserModel:
    @staticmethod
    def get_user(user_id):
        conn = sqlite3.connect('data/documents.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return {"user_id": user[0], "request_count": user[1]} if user else None

    @staticmethod
    def update_request_count(user_id):
        conn = sqlite3.connect('data/documents.db')
        cursor = conn.cursor()
        user = UserModel.get_user(user_id)
        
        if user:
            cursor.execute('UPDATE users SET request_count = request_count + 1 WHERE user_id = ?', (user_id,))
        else:
            cursor.execute('INSERT INTO users (user_id, request_count) VALUES (?, 1)', (user_id,))
        
        conn.commit()
        conn.close()
