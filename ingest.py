import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(data_dir="documents"):
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append({
                "source": filename,
                "text": text
            })
    print(f"Loaded {len(documents)} documents")
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["text"])
        for i, split in enumerate(splits):
            chunks.append({
                "source": doc["source"],
                "chunk_index": i,
                "text": split
            })
    
    print(f"Produced {len(chunks)} chunks")
    return chunks

def inspect_chunks(chunks, n=5):
    print(f"\n--- Sample Chunks ---")
    import random
    samples = random.sample(chunks, min(n, len(chunks)))
    for chunk in samples:
        print(f"\nSource: {chunk['source']} | Index: {chunk['chunk_index']}")
        print(f"Text: {chunk['text']}")
        print(f"Length: {len(chunk['text'])} chars")
        print("-" * 40)

if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents)
    inspect_chunks(chunks)