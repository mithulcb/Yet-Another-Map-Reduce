
import socket	
import pickle
import math	
import shutil
import os
from filesplit.split import Split

#creating socket to accept connection from master_node
s = socket.socket()		
port = 12345			
s.connect(('127.0.0.1', port))
print("CLIENT_MASTER")
status= True

workers=int(input("Enter number of workers:"))
#sends number of workers to be created to master node
s.send(pickle.dumps(workers))


#defining lists to hold socket connection for each client-worker node
#till line 43 it is the same working as master node connection to worker
sock_name=[]
connection=[]
address=[]
worker_port=[]
initial_port=22346	

for i in range(workers):
    sock_name.append("s"+str(i+1))
    connection.append("c"+str(i+1))
    address.append("addr"+str(i+1))
    worker_port.append(initial_port)
    initial_port+=1

for i in range(0,workers):
    sock_name[i]=socket.socket()
    sock_name[i].bind(('', worker_port[i]))
    print ("socket binded to %s" %(worker_port[i]))
    sock_name[i].listen(5)	
    print ("socket is listening")
    connection[i],address[i] = sock_name[i].accept()	
    print ('Got connection from', address[i] )

#function will partition file based on size and number of workers.
#size of file is found usong the os library and size of partitioned file will be (file size/no of workers)
def partition(worker,path_to_file):
    f= open(path_to_file,"r")
    size=os.path.getsize(path_to_file)
    byte_per=math.ceil(size/len(worker))
    list_partition=[]
    for i in range(len(worker)):
        x=f.readlines(byte_per)
        list_partition.append(x)
    return list_partition
    
status1=1


#here user will interact with the client stating what operation will be reuired
while status==True:
    
    print("1->WRITE\n2->READ\n3->MAP-REDUCE\n4->QUIT")
    x=int(input("Enter choice here:"))
    if x==1:
        #for write operation we will send a list of operation,input file path to master node
        operation="W"
        path_to_input=input("ENTER path to input file:")            
        data=pickle.dumps([operation,path_to_input])
        s.send(data)
        data=s.recv(1024)
        data1=pickle.loads(data)
        print(data1)
        # printing list of worker ports returned by master (master worker ports)
        
        info = partition(data1,path_to_input)
        #partioned data is sent to each worker to be stored
        for i in range(len(data1)):
            connection[i].send(pickle.dumps([path_to_input,info[i]]))
        data1=[]


    elif x==2:
        #for write operation we will send a list of operation,input file path to master node
        operation="R"
        path_to_input=input("ENTER path to input file:")
        data=pickle.dumps([operation,path_to_input])
        s.send(data)
        data1=pickle.loads(s.recv(1024)) #worker nodes recieved from master
        
        #for active worker nodes, sends input file path to be read
        for i in range(len(data1)):
            connection[i].send(pickle.dumps(path_to_input))

        #recieves the partially read file from each node and prints it one at a time
        for i in range(len(data1)):
            to_display=connection[i].recv(1024)
            to_display=pickle.loads(to_display)
            for j in to_display:
                print(j.strip("\n"))
        data1=[]

    elif x==3:
        #for a map-reduce operation we send the inputfile,mapperfile,reducerfile to the master npde
        operation="MR"
        path_to_input=input("Enter path to input file:")
        path_to_mapper=input("Enter path to mapper file:")
        path_to_reducer=input("Enter path to reducer file:")
        data=pickle.dumps([operation,path_to_input,path_to_mapper,path_to_reducer])
        s.send(data)
    else:
        data=pickle.dumps(["BYE"])
        s.send(data)
        status=False
    

s.close()	
	
