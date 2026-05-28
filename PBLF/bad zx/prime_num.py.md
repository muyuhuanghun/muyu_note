```
import sys  
  
def is_prime(n):  
    if n < 2:  
        return False  
    if n == 2:  
        return True  
    if n % 2 == 0:  
        return False  
    i = 3  
    while i * i <= n:  
        if n % i == 0:  
            return False  
        i += 2  
    return True  
  
def main():  
    left = int(sys.argv[1])  
    right = int(sys.argv[2])  
  
    primes = []  
    for num in range(left, right + 1):  
        if is_prime(num):  
            primes.append(num)  
  
    with open("output.txt", "w", encoding="utf-8") as f:  
        f.write(str(len(primes)) + "\n")  
        f.write(",".join(map(str, primes)))  
  
if __name__ == "__main__":  
    main()
```

