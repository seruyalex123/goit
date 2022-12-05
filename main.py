import sys

path = None
try:
    path = sys.argv[1]
except IndexError:
    print("No param")

print(path)