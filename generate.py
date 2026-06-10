import os
from dotenv import load_dotenv
from groq import Groq
from embed import embed_and_store, retrieve
from ingest import load_documents, chunk_documents

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query, collection):
    chunks = retrieve(query, collection)
    
    context = ""
    sources = []
    for chunk in chunks:
        context += f"\n---\n{chunk['text']}\n"
        if chunk['source'] not in sources:
            sources.append(chunk['source'])
    
    prompt = f"""You are a helpful assistant that answers questions about the CS program at Stevens Institute of Technology.

Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer the question, say "I don't have enough information on that."
Do not use any outside knowledge. Always cite which document your answer came from.

Documents:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }

if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)
    collection = embed_and_store(chunks)
    
    # Test with evaluation queries
    test_queries = [
        "What do students say about internship opportunities at Stevens?",
        "What are Professor Zumrut's exams like?",
        "What is the weather like on Mars?"  # out of scope test
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("=" * 50)
        result = generate_answer(query, collection)
        print(f"Answer: {result['answer']}")
        print(f"\nSources: {', '.join(result['sources'])}")
        print()