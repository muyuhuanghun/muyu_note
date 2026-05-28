```
import sys  
import json  
  
def main():  
    input_file = sys.argv[1]  
  
    with open(input_file, "r", encoding="utf-8") as f:  
        text = f.read()  
  
    filtered = "".join(ch.lower() for ch in text if ch.isalpha())  
    is_palindrome = "true" if filtered == filtered[::-1] else "false"  
  
    output = {  
        "palindrome": is_palindrome,  
        "result": filtered  
    }  
  
    with open("output.json", "w", encoding="utf-8") as f:  
        json.dump(output, f, ensure_ascii=False, separators=(",", ":"))  
  
if __name__ == "__main__":  
    main()
```