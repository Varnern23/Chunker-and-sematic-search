#base index builder that all others which were made for testing are based from
#imports everything needed to read embedd and then save our chunks as well as the chunker we are using.
import numpy as np
import json
import ollama
from chunker import chunkAholic
#calls our chunker to chunk the text in the file location
chunks = chunkAholic("/home/nathan.varner/Documents/dsc360/lab03/data/book.txt")
#an array we will use to store our chunk embeddings
embeddings = []
#goes through all the chunks and looks at the text of each chunk to embed we then get a vector which will go into the aformentioned embeddings array
for chunk in chunks: 
    chunkText = chunk["text"]
    resp = ollama.embed(model = "mxbai-embed-large", input = chunkText)
    vec = resp["embeddings"][0]
    embeddings.append(vec)
#gets the embeddings into the data type we desire and then normalizes the values.
embeddings = np.array(embeddings, dtype = np.float32)
embeddings = embeddings / np.linalg.norm(embeddings, axis = 1, keepdims = True)
#we now save our information into a chunks file to see all the chunks in json form and our npy file to store the embedding information
np.save("index/embeddings.npy", embeddings)
with open("index/chunks.json", "w") as f:
    for chunk in chunks:
        json.dump(chunk, f)
        f.write("\n")
#stores metadata for our embedding
metadata = {
    "model": "mxbai-embed-large",
    "dimension": embeddings.shape[1],
    "normalized": True,
    "chunker":{
        "targetMin": 1200,
        "targetMax": 1600,
        "minWords": 50,
        "overlapSentences": 1
    }
}
#creates a file to hold said metadata and puts it in there.
with open("index/metadata.json", "w") as f:
    json.dump(metadata, f, indent = 2)
#Help gotten from NumPy doccumentation
