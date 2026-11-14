#File1 Дана строка S. Если S — допустимое имя файла, создать пустой файл с этим именем и вывести True, иначе False

import os

S = input()

if '/' in S or '\\' in S:
    print(False)
else:
    try:
        with open(S, 'x'):
            pass
        print(True)
    except (FileExistsError, OSError):
        print(False)
