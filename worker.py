import socket	
import pickle
from subprocess import run
import sys
import os

#using sys library we extract the arguments provided in call function
w=int(sys.argv[1])
port=int(sys.argv[2])
port_c=int(sys.argv[3])
no=int(sys.argv[4])



#using subprocessing, call mapper with arguments
def callpy(x,path,save1):
            run("Python3 {} {} {}".format(path,str(save1),x),input=x.encode())

#using subprocessing, call shuffle with arguments
def callshuffle(x,path,save1,no_wrk):
    run("Python3 {} {} {} {}".format(path,str(save1),no_wrk,x),input=x.encode())

#using subprocessing, call reducer with arguments
def callred(x,path,save1):
    run("Python3 {} {} {}".format(path,str(save1),x),input=x.encode())

s = socket.socket()		



path_to_shuffle="map-red/shuffle.py"

#connects to master
s.connect(('127.0.0.1', port))
print("worker"+str(w)+" master")

con=1
#connects to client
c = socket.socket()
c.connect(('127.0.0.1', port_c))
print("worker"+str(w)+" Client")
con=0

#fill path to desired directory to create folder
path_to_folder=""
folder_name="worker"+str(w)

path = os.path.join(path_to_folder, folder_name)
os.mkdir(path)
print("Worker"+str(w)+" created directory "'% s'% folder_name)



while True:
    
    x=pickle.loads(s.recv(1024))
    #recieves start command for w operation
    if x=="START":
        data=c.recv(1024) #partitioned data recieved
        data=pickle.loads(data)
        #manipulating recieved path to form new file path to be stored in
        #input.txt -> input1.txt
        x=data[0]
        l=x.split(".")
        new_x="worker"+str(w)+"/"+l[0]+str(w)+"."+l[1]
        #opeing file and writing patial information to it
        with open(new_x, "w") as output:
            for i in data[1]:
                output.write(i)
    
    elif x=="START1":
        #recieves start command for r operation
        data=c.recv(1024)
        data=pickle.loads(data)
        print(data)
        l=data.split(".")
        #mainpulating path to access the partition file
        new_x="worker"+str(w)+"/"+l[0]+str(w)+"."+l[1]
        f=open(new_x,"r")
        info=f.readlines()
        #reading the partition files and sending information to client
        c.send(pickle.dumps(info))

    elif x=="START2":
        l=pickle.loads(s.recv(1024))
        path_to_w=l[0]
        path_to_w=path_to_w.split(".")
        #input1.txt
        l[0]="worker"+str(w)+"/"+path_to_w[0]+str(w)+"."+path_to_w[1]
        #manipulating to form input1partial.txt where mapper o/p stored
        save="worker"+str(w)+"/"+path_to_w[0]+str(w)+"partial"+"."+path_to_w[1]
        f=open(l[0],"r")
        info=f.read()
        callpy(info,l[1],save)  #l[1] is path to mapper and save where we want to save ie inpu1partial.txt
        s.send(pickle.dumps("ACK")) #sends ACK once mapper is completed
        no_wrk=pickle.loads(s.recv(1024))
        #manipulating to form input1shuffle.txt where shuffler o/p store
        shuffle_save="worker/"+path_to_w[0]+"shuffle"+"."+path_to_w[1]
        new_f=open(save,"r")
        new_info=new_f.read()
        #call shuffle
        callshuffle(new_info,path_to_shuffle,shuffle_save,no_wrk)
        s.send(pickle.dumps("ACK1"))#sends ACK once shuffle is completed
        save_shuffle="worker"+str(w)+"/"+path_to_w[0]+str(w)+"shuffle"+"."+path_to_w[1]
        f_final=open(save_shuffle,"r")
        #sorting shuffle output before passing into reducer
        x = f_final.readlines()
        x.sort()
        new_x=""
        for i in x:
            new_x+=i
        #call reduce
        callred(new_x,l[2],"worker"+str(w)+"/part-0000")
        s.send(pickle.dumps("ACK2"))#sends ACK once reducer is completed
        s.send(pickle.dumps("worker"+str(w)+"/part-0000"))
   
s.close()	

