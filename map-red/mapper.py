import sys

print(sys.argv[1])
save=sys.argv[1]
f=open(save,"a")

for line in sys.stdin:
    words = line.lower().strip().split()
    for word in words:
        print(f"{word},1")
        f.write(f"{word},1"+"\n")