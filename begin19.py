x1 = float(input())
y1 = float(input())
x2 = float(input())
y2 = float(input())

width = abs(x2 - x1)
length = abs(y2 - y1)

P = 2 * (width + length)
S = width * length

print(P)
print(S)