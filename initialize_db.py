import sqlite3
from app.models import DocumentModel

conn = sqlite3.connect('data/documents.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        embedding BLOB
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        request_count INTEGER
    )
''')

conn.commit()

sample_documents = [
    "Artificial intelligence is transforming the world by enabling machines to learn from data.",
    "Machine learning is a subset of AI that focuses on building algorithms that can learn and make predictions.",
    "Data science combines domain knowledge, programming skills, and statistics to extract insights from data."
]

for doc in sample_documents:
    DocumentModel.add_document(doc)

print("Database initialized and sample documents inserted!")
