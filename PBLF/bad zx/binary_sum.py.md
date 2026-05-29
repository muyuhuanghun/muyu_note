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
[[palindrome_check.py]]
[[highest_freq_elem.py]]
[[json_csv_interconv.py]]
[[palindrome_check.py]]
[[prime_num.py]]
[[str_format.py]]
[[top_n_stu.py]]
[[word_freq.py]]
