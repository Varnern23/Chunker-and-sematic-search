import numpy as np
import json
import ollama
from chunker1000 import chunkAholic

chunks = chunkAholic("/home/nathan.varner/Documents/dsc360/lab03/data/book.txt")
embeddings = []
for chunk in chunks: 
    chunkText = chunk["text"]
    resp = ollama.embed(model = "nomic-embed-text", input = chunkText)
    vec = resp["embeddings"][0]
    embeddings.append(vec)
embeddings = np.array(embeddings, dtype = np.float32)
embeddings = embeddings / np.linalg.norm(embeddings, axis = 1, keepdims = True)
np.save("index/embeddings21000.npy", embeddings)
with open("index/chunks21000.json", "w") as f:
    for chunk in chunks:
        json.dump(chunk, f)
        f.write("\n")
metadata = {
    "model": "nomic-embed-text",
    "dimension": embeddings.shape[1],
    "normalized": True,
    "chunker":{
        "targetMin": 600,
        "targetMax": 1000,
        "minWords": 50,
        "overlapSentences": 1
    }
}
with open("index/metadata21000.json", "w") as f:
    json.dump(metadata, f, indent = 2)
