from pathlib import Path
import re
import statistics

def chunkAholic(filePath, minChar = 1200, maxChar = 3000, minWord = 50):
    with open(filePath, "r", encoding = "utf-8") as file:
        content = file.read()
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()] 
        chunks = []
        chunkID = 0
        splits = 0
        charIndex = 0
        for paragraph in paragraphs:
            startIndex = content.find(paragraph, charIndex)
            endIndex = startIndex + len(paragraph)
            charIndex = startIndex + len(paragraph)
            if len(paragraph) <= maxChar:
                chunks.append({
                    'ID': chunkID,
                    'text': paragraph.replace("\n", " ").strip(),
                    'start': startIndex,
                    'end': charIndex
                })
                chunkID += 1
            else:
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                between = []
                current = ""
                last = ""
                for sentence in sentences:
                    shrek = (current + " " + sentence).strip()
                    if len(shrek) > maxChar and current:
                        chunks.append({
                            'ID': chunkID,
                            'text': current.replace("\n", " ").strip(),
                            'start': startIndex,
                            'end': startIndex + len(current.strip()) 
                        })
                        chunkID += 1
                        splits += 1
                        current = last + " " + sentence
                    else:
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
