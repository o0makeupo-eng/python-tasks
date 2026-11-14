#File4 Даны имена четырёх файлов. Найти количество существующих среди них в текущем каталоге

import os

files = [input() for _ in range(4)]
count = sum(1 for f in files if os.path.isfile(f))
print(count)
