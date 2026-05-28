```
import sys  
import json  
  
def main():  
    input_file = sys.argv[1]  
  
    with open(input_file, "r", encoding="utf-8") as f:  
        data = json.load(f)  
  
    data_tuple = tuple(data)  
  
    freq = {}  
    for item in data_tuple:  
        freq[item] = freq.get(item, 0) + 1  
  
    max_count = max(freq.values())  
    result = [str(k) for k, v in freq.items() if v == max_count]  
  
    with open("output.txt", "w", encoding="utf-8") as f:  
        f.write(",".join(result))  
  
if __name__ == "__main__":  
    main()
```