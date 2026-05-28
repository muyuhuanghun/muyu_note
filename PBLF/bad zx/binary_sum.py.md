```
import sys  
  
  
def main():  
    binary_args = sys.argv[1:]  
  
    # 初始化总和为 0    total_sum = 0  
  
    for bin_str in binary_args:  
        total_sum += int(bin_str, 2)  
  
    result_str = bin(total_sum)[2:]  
  
    print(result_str)  
  
  
if __name__ == "__main__":  
    main()
```
