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

<h1>STRUCTURE</h1>
![image](https://user-images.githubusercontent.com/78469903/205070963-8c3a8f29-4f4c-4416-89b3-198198ccc2e4.png)

<h3>WORKFLOW OF WRITE</h3>
![image](https://user-images.githubusercontent.com/78469903/205071214-30b65862-092b-4ace-9cfd-a9ebac5d4c20.png)



<h3>WORKFLOW OF READ</h3>
![image](https://user-images.githubusercontent.com/78469903/205071296-2aa96bc7-175b-4a11-be58-375a64b3305c.png)



<h3>WORKFLOW OF MAP-REDUCE</h3>
<h4>MAP PHASE</h4>
![image](https://user-images.githubusercontent.com/78469903/205071399-8927cd58-48df-454b-bab8-84cab9414a5e.png)
![image](https://user-images.githubusercontent.com/78469903/205071633-4f012d38-fb25-4ef4-a1c4-74347c585a29.png)


<h4>SHUFFLE PHASE</h4>
![image](https://user-images.githubusercontent.com/78469903/205071677-2c2f9fc9-b440-4cee-b8b7-5b04eaa81756.png)


<h4>REDUCER PHASE</h4>
![image](https://user-images.githubusercontent.com/78469903/205071847-aca61869-9227-4602-a78a-3f549f91f539.png)
![image](https://user-images.githubusercontent.com/78469903/205071917-3bb39a4b-e3ca-4f41-9224-2fbd8293f478.png)
![image](https://user-images.githubusercontent.com/78469903/205071987-c835d48f-845f-4a7e-aa92-2981c009f603.png)




