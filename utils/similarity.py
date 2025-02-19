from sklearn.metrics.pairwise import cosine_similarity

def check_uniqueness(new_embedding, collection):
    # :return: Uniqueness score (float between 0 and 1).
    print("Retrieving stored embeddings from ChromaDB...")
    stored_embeddings = collection.get(include=["embeddings"])["embeddings"]
    print(f"Stored embeddings count: {len(stored_embeddings)}")
    
    max_similarity = 0.0
    for emb in stored_embeddings:
        similarity = cosine_similarity([new_embedding], [emb])[0][0]
        print(f"Similarity with stored document: {similarity}")
        max_similarity = max(max_similarity, similarity)
    
    # Calculate uniqueness as 1 - max_similarity
    uniqueness_score = round((1 - max_similarity)*100)
    print(f"Uniqueness score: {uniqueness_score}/100")
    return uniqueness_score