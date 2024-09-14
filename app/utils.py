from sentence_transformers import SentenceTransformer
from redis import Redis

model = SentenceTransformer('all-MiniLM-L6-v2')
redis_cache = Redis(host='localhost', port=6379)

def encode_text(text):
    return model.encode([text])[0]

def cache_response(query, response):
    redis_cache.set(query, str(response))

def retrieve_from_cache(query):
    cached_response = redis_cache.get(query)
    return eval(cached_response) if cached_response else None
