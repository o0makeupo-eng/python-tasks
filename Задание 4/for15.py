a = float(input())
n = int(input())
total = 1
for i in range(1, n + 1):
    total *= a ** i
print(total)
