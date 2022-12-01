# BD2_198_214_284_291
Repo created programmatically. Project Title: Yet another MapReduce (YaMR)

networking setup:
first we connect master to client
client takes number of workers as input and sends it to the master
Then we define ports , connections ,addresses and worker_ports  for number of workers
Then we connect worker to master and worker to client 

There are 4 operations :
1)read 
2)write
3)map-reduce
4)quit


1)read:

input path to input file 
client sends the path to input file to master and will recieve worker nodes
after we recieve worker nodes , we will read from all the worker nodes and display the file 
as master gets input as R it will send start1 to the worker nodes and the worker will read from the file which was created during write (worker1_input.txt) and send it to the client , so all the workers will send their files and we concatinate it and print the contents


2)write:

input path to input file 
client sends the path to input file to master and will recieve worker nodes ports , we then partition the input.txt and send it to different worker nodes.Start will be sent to worker from master.Once start is recieved , we then recieve the partitioned data and we create a new file (worker_input1.txt) and write the partitioned data to it


3)map-reduce:

input path to input file 
input path to mapper file 
input path to reducer file 

we send these inputs with operation as map-reduce to the master and master will send start2 to the worker nodes , worker nodes will perform mapper and the partial outputs are sent to shuffler which will shuffle based on a particular hash function which will be sent to reducer.Each worker sends Ack once the mapper the mapper is completed on a worker node , and once master recieves acks = no of worker nodes it prints map completed.So there will be partial mapper files ,partial shuffler files , partial reducer files. We sort the partial shuffler files and send to reducer,so the partial output files will be stored in each worker folder and we combine all these files to give the output.Every worker sends Ack once reducer is complete and if no of acks = no of worker nodes then we say map-reduce complete




4)quit : 

Kills all the worker nodes , client node , master node

