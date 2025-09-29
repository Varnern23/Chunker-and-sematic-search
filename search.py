import numpy as np
import json
from ollama import embed
import csv


with open("index/metadata2.json", "r") as f:
    metadata = json.load(f)

with open("index/chunks2.json", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
embeddings = np.load("index/embeddings2.npy")
k = 5
print("Type your query or type exit to quit:\n")
labels = ["prompt", "expected", "hit 1", "hit 2", "hit 3", "hit 4", "hit 5"]
with open("outputs/baseTest.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(labels)
    while True:
        query = input("Enter query: ")
        if query.lower() == "exit":
            break
        resp = embed(model=metadata["model"], input=query)
        qVector = np.array(resp["embeddings"][0], dtype=np.float32)
        qVector /= np.linalg.norm(qVector)
        scores = np.dot(embeddings, qVector)
        topK = np.argsort(scores)[-k:][::-1]
        print("\n Top Chunks:\n")
        track = set()
        hits = []
        for rank, i in enumerate(topK, start=1):
            i = int(i)
            chunk = chunks[i]
            chunkID = chunk['ID']
            if chunkID in track:
                continue
            track.add(chunkID)
            hits.append(chunk)
            print(f"Rank: {rank}, Score: {scores[i]:.4f}")
            print(f"Chunk ID: {chunk["ID"]}\n")
            print(f"Text: {chunk["text"]}")
        print("\n")
        writer.writerow( [query, "", 
                         hits[0]['text'],
                         hits[1]['text'],
                         hits[2]['text'],
                         hits[3]['text'],
                         hits[4]['text']])
