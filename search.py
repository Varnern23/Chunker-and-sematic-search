#sematic searcher program using the embeddings made in build index
import numpy as np
import json
from ollama import embed
import csv

## if you wanna switch what embedding you use just change metadata2 to metadata and vice versa for chunks and embeddings below
## also change the csv filw to another one when switching models
#loads metadata of embedding model and chunker so we can see it
with open("index/metadata2.json", "r") as f:
    metadata = json.load(f)
#just some of the prompts we used to test the searcher on moby dick
testingPrompts = ["Father Mapple delivers a powerful sermon about Jonah and the whale", "Captain Ahab gives his quarter-deck speech about killing the whale", "Queequeg becomes ill and has the ship's carpenter build him a coffin", "Captain Ahab's final words", "Ishmael explains what a gam is", "Ishmael and Queequeg cuddle in bed"]
#reads our chunks so we know what to output
with open("index/chunks2.json", "r", encoding="utf-8") as f:
    chunks = [json.loads(line) for line in f]
#loads in our embeddings so we can calc distance
embeddings = np.load("index/embeddings2.npy")
#sets how many possible chunks we want back
k = 5
#puts in a query if you were not ussing testing prompts if you were not you would just add the line query = input("whats the query") later after the loop starts
print("Type your query or type exit to quit:\n")
#organization for our returned csv file
labels = ["prompt", "expected id", "id 1", "hit 1", "id 2", "hit 2", "id 3", "hit 3", "id 4", "hit 4", "id 5", "hit 5", "in 1", "in 5"]
#opens the csv file we are modifying to return our results.
with open("outputs/baseTest.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(labels)
    #if using personal queries just set to while true instead of testing prompts
    for query in testingPrompts:
        #exits the program assuming you were using your own prompts
        if query.lower() == "exit":
            break
        #here we are embedding the query to compare the distances between our prompt and the other already embedded chunks we do get the query vector into the right format as well as normalizing it before comparing distances.
        resp = embed(model=metadata["model"], input=query)
        qVector = np.array(resp["embeddings"][0], dtype=np.float32)
        qVector /= np.linalg.norm(qVector)
        scores = np.dot(embeddings, qVector)
        #no we get into returning the chunks with the best score
        topK = np.argsort(scores)[-k:][::-1]
        print("\n Top Chunks:\n")
        #used to keep track of which chunk we are on when out puting the chunks into the csv file
        track = set()
        hits = []
        #sets up a counter and goes through every one of our top k answers outputung them into the terminal along with important data.
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
        #writes out info to the csv file we are using
        writer.writerow( [query, "", 
                            hits[0]['ID'],
                            hits[0]['text'],
                            hits[1]['ID'],
                            hits[1]['text'],
                            hits[2]['ID'],
                            hits[2]['text'],
                            hits[3]['ID'],
                            hits[3]['text'],
                            hits[4]['ID'],
                            hits[4]['text'],
                            "", ""])
        #help from numpy, python, and csv doccumentation and some aid from geeks for geeks about some ssimple stuff in python I wasn't familiar with like enumerate
