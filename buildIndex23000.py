import numpy as np
import json
import ollama
from chunker3000 import chunkAholic

chunks = chunkAholic("/home/nathan.varner/Documents/dsc360/lab03/data/book.txt")
embeddings = []
for chunk in chunks: 
    chunkText = chunk["text"]
    resp = ollama.embed(model = "nomic-embed-text", input = chunkText)
    vec = resp["embeddings"][0]
    embeddings.append(vec)
embeddings = np.array(embeddings, dtype = np.float32)
embeddings = embeddings / np.linalg.norm(embeddings, axis = 1, keepdims = True)
np.save("index/embeddings23000.npy", embeddings)
with open("index/chunks23000.json", "w") as f:
    for chunk in chunks:
        json.dump(chunk, f)
        f.write("\n")
metadata = {
    "model": "nomic-embed-text",
    "dimension": embeddings.shape[1],
    "normalized": True,
    "chunker":{
        "targetMin": 1200,
        "targetMax": 3000,
        "minWords": 50,
        "overlapSentences": 1
    }
}
with open("index/metadata23000.json", "w") as f:
    json.dump(metadata, f, indent = 2)
