#imports our necessary libraries in order to read files and easily calculate some thinsg for testing.
from pathlib import Path
import re
import statistics
#defines function amd sets ideal min characters a hard max characters and a minimum word count. Which honestly doesnt really work
def chunkAholic(filePath, minChar = 1200, maxChar = 1600, minWord = 50):
    #opening a file to chunk in this instance moby dick and sets up some pointers and holding variables
    with open(filePath, "r", encoding = "utf-8") as file:
        content = file.read()
        #cuts the book into paragraphs by looking for empty spaces
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()] 
        chunks = []
        chunkID = 0
        splits = 0
        charIndex = 0
        # we the look through all the paragraphs we made and assign them values that will be stored as metadata for the chunk as well as the chunks ID
        for paragraph in paragraphs:
            startIndex = content.find(paragraph, charIndex)
            endIndex = startIndex + len(paragraph)
            charIndex = startIndex + len(paragraph)
            #if the chunk is less then the max size we just insert it with given meta data
            if len(paragraph) <= maxChar:
                chunks.append({
                    'ID': chunkID,
                    'text': paragraph.replace("\n", " ").strip(),
                    'start': startIndex,
                    'end': charIndex
                })
                chunkID += 1
                #if the chunk is to big we split it into sentences which we will then restructure into good sized chunks
            else:
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                between = []
                current = ""
                last = ""
                for sentence in sentences:
                    shrek = (current + " " + sentence).strip()
                    #if we find that adding the next sentence to the current prompt canidate will make it to big we call it a day and it becomes a chunk.
                    if len(shrek) > maxChar and current:
                        chunks.append({
                            'ID': chunkID,
                            'text': current.replace("\n", " ").strip(),
                            'start': startIndex,
                            'end': startIndex + len(current.strip()) 
                        })
                        chunkID += 1
                        splits += 1
                        #this creates overlap between chunks of a sentence and allows more context in the chunks
                        current = last + " " + sentence
                    else:
                        #if the canidate is not too big after adding the next sentence then we just keep looking until the end of the larger chunk
                        current = shrek
                    last = sentence
                if current.strip():
                    chunks.append({
                        'ID': chunkID,
                        'text': current.strip(),
                        'start': endIndex - len(current.strip()),
                        'end': endIndex 
                    })
                    chunkID += 1
        # pretty sure this is mostly useless here and realized it should probably go after merged so you can just ignore this part.
        fixedChunks = [] 
        for chunk in chunks:
            if len(chunk["text"]) > maxChar:
               text = chunk["text"]
               for i in range(0, len(text), maxChar):
                    part = text[i:i+maxChar]
                    fixedChunks.append({
                        'ID': chunkID,
                        'text': part.strip(),
                        'start': chunk['start'] + i,
                        'end': chunk['start'] + i + len(part)
                    })
                    chunkID += 1
            else:
                fixedChunks.append(chunk)
        # we then go through all the chunks that were too small and combine them to make bigger chunks.
        merged = []
        between = None
        for chunky in fixedChunks:
            if len(chunky["text"].split()) < minWord:
                if between:
                    between["text"]+= " " + chunky["text"]
                    between["end"] = chunky["end"]
                else:
                    between = chunky
            else:
                if between: 
                    between["text"] += " " + chunky["text"]
                    between["end"] = chunky["end"]
                    merged.append(between)
                    between = None
                else:
                    merged.append(chunky)
        if between:
            merged.append(between)
        # We then go through the merged chunks list and enforce the max character capacity
        final = []
        for chunkster in merged:
            text = chunkster["text"]
            if len(text) > maxChar:
                for i in range(0, len(text), maxChar):
                    part = text[i:i+maxChar]
                    final.append({
                        'ID': chunkID,
                        'text': part.strip(),
                        'start': chunkster['start'] + i,
                        'end': chunkster['start'] + i + len(part)
                    })
                    chunkID += 1
            else:
                final.append(chunkster)
        # we then have some sanity tests just for checking
        lengths = [len(c['text']) for c in final]
        print("sanity check:")
        print(f"Total Chunks: {len(final)}")
        print(f"Total Splits: {splits}")
        print(f"Average Chunk Length: {int(statistics.mean(lengths))}")
        print(f"minimum Chunk Length: {min(lengths)}")
        print(f"maximum Chunk Length: {max(lengths)}")
        return final
if __name__ == "__main__":
    file_path = "/home/nathan.varner/Documents/dsc360/lab03/data/book.txt"
    chunks = chunkAholic(file_path)
    print(chunks[1200])
