import numpy as np
import json
from ollama import embed

with open("index/metadata.json", "r") as f:
    metadata = json.load(f)

with open("index/chunks.json", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
embeddings = np.load("index/embeddings.npy")
k = 5
print("Type your query or type exit to quit:\n")
while True:
    query = input("Enter query: ")
    if query.lower() == "exit":
        break
    resp = embed(model = metadata["model"], input = query)
    qVector = np.array(resp["embeddings"][0], dtype = np.float32)
    qVector /= np.linalg.norm(qVector)
    scores = np.dot(embeddings, qVector)
    topK = np.argsort(scores)[-k:][::-1]
    print("\n Top Chunks:\n")
    track = set()
    for rank, i in enumerate(topK, start = 1):
        i = int(i)
        chunk = chunks[i]
        chunkID = chunk['ID']
        if chunkID in track:
            continue
        track.add(chunkID)
        print(f"Rank: {rank}, Score: {scores[i]:.4f}")
        print(f"Chunk ID: {chunk['ID']}")
        print(f"Text: {chunk['text']}\n")
    
