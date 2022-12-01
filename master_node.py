
import socket		
import pickle	
from subprocess import call
from subprocess import PIPE, Popen, STDOUT, TimeoutExpired

#creating client-master connection
s = socket.socket()		
print ("Socket successfully created")
port = 12345
s.bind(('', port))		
print ("Client Node socket binded to %s" %(port))
s.listen(5)	
print ("Client Node socket is listening")
#waiting for client side connection
c, addr = s.accept()	
print ('Got connection from', addr )

print("CLIENT_MASTER")

#recieves number of desired workers
workers=pickle.loads(c.recv(1024))

#defining lists to hold socket connection for each master-worker node
sock_name=[]
connection=[]
address=[]
worker_port1=[] #holds port number for master connection to worker
worker_port2=[] #holds port number for client connection to worker
initial_port1=12346
initial_port2=22346


for i in range(workers):
    #creating list size of number of workers
    sock_name.append("s"+str(i+1)) 
    connection.append("c"+str(i+1))
    address.append("addr"+str(i+1))
    worker_port1.append(initial_port1)
    worker_port2.append(initial_port2)
    initial_port1+=1
    # worker to master
    initial_port2+=1 
    # worker to client

i=0
# master to worker
for i in range(workers): 
    #dynamically creating a socket and storing it in the index of the previously defined lists, 
    sock_name[i]=socket.socket()
    sock_name[i].bind(('', worker_port1[i]))
    print ("W"+str(i),"socket binded to %s" %(worker_port1[i]))
    sock_name[i].listen(5)
    #waiting for worker connection
    print ("socket is listening")
    #using pipes we will execute the below command on a sep terminal for each worker respectively
    # python3 worker.py 1 12346 22346 4
    cmd="Python3 {} {} {} {} {}".format("worker.py",i+1,worker_port1[i],worker_port2[i],workers)
    #argumnets in order are:path to worker file,worker number,port for master-worker connection,port for client-worker connection and number of workers to be set up
    process_machine = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    # will execute cmd on sep terminal

    #ecieves connection from worker
    connection[i],address[i] = sock_name[i].accept()	
    print ('Got connection from', address[i] )

ack=0
ack1=0
ack2 =0
while True:

    
    data = c.recv(1024)
    recvd=pickle.loads(data)
    print(f"Received {recvd!r}")
    if recvd[0]=="W":
        #if write command recieved will send a list of active worker nodes to client 
        data=pickle.dumps(worker_port1[0:workers])
        c.send(data)
        for i in range(workers):
            data1=pickle.dumps("START")
            connection[i].send(data1)
            # start command for w sent to workers
    
    if recvd[0]=="R":
        #if read command recieved will send a list of active worker nodes to client
        data=pickle.dumps(worker_port1[0:workers])
        c.send(data)
        for i in range(workers):
            data1=pickle.dumps("START1")
            # start1 command for r sent to workers
            connection[i].send(data1)
    
    elif recvd[0]=="MR":
        for i in range(workers):
            # start2 command for w sent to workers
            data1=pickle.dumps("START2")
            connection[i].send(data1)
        for i in range(workers):
            data2=pickle.dumps(recvd[1:])
            connection[i].send(data2)
        for i in range(workers):
            msg=connection[i].recv(1024)
            if pickle.loads(msg)=="ACK":
                ack+=1
        if ack==workers:
            print("MAP COMPLETED")
            ack=0
        for i in range(workers):
            data3=pickle.dumps(workers)
            connection[i].send(data3)
        print("worker info sent")
        for i in range(workers):
            msg=connection[i].recv(1024)
            if pickle.loads(msg)=="ACK1":
                ack1+=1
        if ack1==workers:
            print("SHUFFLE COMPLETED")
            ack1=0
        for i in range(workers):
            msg=connection[i].recv(1024)
            if pickle.loads(msg)=="ACK2":
                ack2+=1
        if ack2==workers:
            print("REDUCE COMPLETED")
            print("MAP-REDUCE COMPLETED")
            ack2=0
        f=open("part-0000","w")
        dir="worker"
        for i in range(workers):
            new_dir=dir+str(i+1)+"/part-0000"
            f1=open((new_dir),"r")
            f.write(f1.read())
            f1.close()
            new_dir=''
        f.close()

        pass
    
    if not data:
        break
    try:
        c.sendall(data)
    except:
        break


