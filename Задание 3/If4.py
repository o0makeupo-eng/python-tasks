a = int(input())
b = int(input())
c = int(input())
count = (a > 0) + (b > 0) + (c > 0)
if count == 1:
    print(1)
elif count == 2:
    print(2)
elif count == 3:
    print(3)
else: 
    print(0)
