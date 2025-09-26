from pathlib import Path
import re
import statistics

def chunkAholic(filePath, minChar = 1200, maxChar = 1600, minWord = 50):
    with open(filePath, 'r') as file:
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
        merged = []
        between = None
        for chunk in chunks:
            if len(chunk["text"].split()) < minWord:
                if between:
                    between["text"]+= "" + chunk["text"]
                    between["end"] = chunk["end"]
                else:
                    between = chunk
            else:
                if between: 
                    between["text"] += " " + chunk["text"]
                    between["end"] = chunk["end"]
                    merged.append(between)
                    between = None
                else:
                    merged.append(chunk)
        if between:
            merged.append(between)
        
        lengths = [len(c['text']) for c in merged]
        print("sanity check:")
        print(f"Total Chunks: {len(merged)}")
        print(f"Total Splits: {splits}")
        print(f"Average Chunk Length: {int(statistics.mean(lengths))}")
        print(f"minimum Chunk Length: {min(lengths)}")
        print(f"maximum Chunk Length: {max(lengths)}")

        return merged


if __name__ == "__main__":
    file_path = "/home/nathan.varner/Documents/dsc360/lab03/data/book.txt"
    chunks = chunkAholic(file_path)
    print(chunks[410])
