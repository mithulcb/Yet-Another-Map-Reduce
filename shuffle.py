import sys

save=sys.argv[1]
save_name=save.split(".")
save_as=save_name[0]
save_worker=save_as.split("/")
save_shuffle=save_worker[1]
save_final=save_shuffle.split("shuffle")
no_wrk=sys.argv[2]



f=[]
check=[]
d={}
for i in range(int(no_wrk)):
    f.append(i)

for i in range(int(no_wrk)):
    f[i]=open(save_worker[0]+str(i+1)+"/"+save_final[0]+str(i+1)+"shuffle"+save_final[1]+"."+save_name[1],"a")
    d[i]=save_worker[0]+str(i+1)+"/"+save_final[0]+str(i+1)+"shuffle"+save_final[1]+"."+save_name[1]
    f[i].close()

for line in sys.stdin:
    words = line.lower().strip().split()
    for word in words:
        l=word.split(",")
        word1=l[0]
        hash_val=ord(word1[0])%int(no_wrk)
        f=open(d[hash_val],"a")
        f.write(word+"\n")
        f.close()