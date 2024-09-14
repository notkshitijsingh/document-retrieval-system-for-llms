from flask import Blueprint, request, jsonify
from .models import DocumentModel, UserModel
from .utils import encode_text, cache_response, retrieve_from_cache

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is active"})


@api_blueprint.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    user_id = data['user_id']
    query = data['text']
    top_k = data.get('top_k', 5)
    threshold = data.get('threshold', 0.5)

    # Rate limiting check
    user = UserModel.get_user(user_id)
    if user and user.request_count >= 5:
        return jsonify({"error": "Rate limit exceeded"}), 429

    # Try retrieving from cache
    cached_response = retrieve_from_cache(query)
    if cached_response:
        return jsonify({"results": cached_response})

    # Encode the query and search in the documents
    query_vector = encode_text(query)
    documents = DocumentModel.get_all_documents()
    
    # Compute similarities
    results = []
    for doc in documents:
        similarity = DocumentModel.calculate_similarity(query_vector, doc['embedding'])
        if similarity >= threshold:
            results.append((doc['text'], similarity))

    # Sort and limit results
    results = sorted(results, key=lambda x: x[1], reverse=True)[:top_k]

    # Cache the response for future requests
    cache_response(query, results)

    # Update user request count
    UserModel.update_request_count(user_id)

    return jsonify({"results": results})
