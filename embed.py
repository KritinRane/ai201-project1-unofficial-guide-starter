import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, chunk_documents

def embed_and_store(chunks):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = chromadb.PersistentClient(path="./chroma_db")
    
    collection = client.get_or_create_collection(name="stevens_reviews")
    
    texts = [chunk["text"] for chunk in chunks]
    sources = [chunk["source"] for chunk in chunks]
    indices = [str(chunk["chunk_index"]) for chunk in chunks]
    ids = [f"{chunk['source']}_{chunk['chunk_index']}" for chunk in chunks]
    
    print(f"Embedding {len(chunks)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    collection.add(
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=[{"source": s, "chunk_index": i} for s, i in zip(sources, indices)],
        ids=ids
    )
    
    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return collection

def retrieve(query, collection, k=5):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    
    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks

if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)
    collection = embed_and_store(chunks)
    
    # Test retrieval with 3 queries
    test_queries = [
        "What do students say about internship opportunities at Stevens?",
        "What are Professor Zumrut's exams like?",
        "What are common complaints about the Stevens CS program?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        results = retrieve(query, collection)
        for r in results:
            print(f"Source: {r['source']} | Distance: {r['distance']:.3f}")
            print(f"Text: {r['text'][:200]}...")
            print()