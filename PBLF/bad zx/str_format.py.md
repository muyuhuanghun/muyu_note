```
import sys  
  
def main():  
    input_file = sys.argv[1]  
    output_file = sys.argv[2]  
  
    result = []  
  
    with open(input_file, "r", encoding="utf-8") as f:  
        for line in f:  
            digits = "".join(ch for ch in line if ch.isdigit())  
            if len(digits) == 9:  
                formatted = digits[:3] + "-" + digits[3:6] + "-" + digits[6:]  
                result.append(formatted)  
  
    with open(output_file, "w", encoding="utf-8") as f:  
        f.write("\n".join(result))  
  
if __name__ == "__main__":  
    main()
```
