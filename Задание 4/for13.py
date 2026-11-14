n = int(input())
total = 0.0
for i in range(1, n + 1):
    v = 1 + i * 0.1
    if i % 2 == 1:
        total += v
    else:
        total -= v
print(total)
