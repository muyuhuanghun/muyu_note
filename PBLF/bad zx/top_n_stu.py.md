```
import sys  
import json  
  
def main():  
    input_file = sys.argv[1]  
    n = int(sys.argv[2])  
  
    with open(input_file, "r", encoding="utf-8") as f:  
        data = json.load(f)  
  
    sorted_students = sorted(data.items(), key=lambda x: x[1], reverse=True)  
    top_students = [name for name, score in sorted_students[:n]]  
  
    with open("output.csv", "w", encoding="utf-8") as f:  
        f.write(",".join(top_students))  
  
if __name__ == "__main__":  
    main()
```

