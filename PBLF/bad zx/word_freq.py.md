```
import sys  
import json  
  
def output(obj):  
    print(json.dumps(obj))  
  
def main():  
    input_file = sys.argv[1]  
  
    with open(input_file, "r", encoding="utf-8") as f:  
        text = f.read()  
  
    text = text.lower()  
    text = text.replace(".", " ")  
    text = text.replace("!", " ")  
    text = text.replace("?", " ")  
  
    words = text.split()  
  
    freq = {}  
    for word in words:  
        freq[word] = freq.get(word, 0) + 1  
  
    output(freq)  
  
if __name__ == "__main__":  
    main()
```

