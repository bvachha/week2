# Week 2 Practice 
* This week follows along with log file analysis and extraction of meaningful statistics from a log file using various tools like bash, perl and python.
* The bash script is a standalone that will need to be run with the path to the logfile as an input parameter to the script. 
* The perl and python applications are fully dockerized web applications that can be deployed using the docker files contained in their respective directories 

## Statistics extracted 
All three methods extract the following statistics from the log file and present it to the user. 

NOTE: PYTHON ONLY GIVES THE REQUEST COUNT FOR LAST 10 MINUTES STATISTICS WHILE PERL AND BASH PROVIDE THE REQUEST INFORMATION WITH DIFFERENT LEVELS OF GRANULARITY. 

1. Statistics by time interval 
    1. Daily Statistics
        1. Most requested host for each day in the log file 
        2. Most requested upstream IP address for each day
        3. Most requested Path(upto 2 levels) for each day
    2. Weekly Statistics (Denoted by week of the year)
        1. Most requested host for each week in the log file 
        2. Most requested upstream IP address for each week
        3. Most requested Path(upto 2 levels) for each week
    3. Monthly Statistics (Denoted by month of the year)
        1. Most requested host for each month in the log file 
        2. Most requested upstream IP address for each month
        3. Most requested Path(upto 2 levels) for each month
2. Total requests by status code
    Returns a summary of the number of times each status code was sent by the server 
3. Top resources by request:
    1. Top 5 upstream IPs : List of top 5 upstream servers with request counts which handled maximum number of requests 
    2. Top 5 Hosts: List of top 5 hosts with request counts which handled maximum number of requests 
    2. Top 5 Response Body Sizes: List of top 5 response body sizes in bytes with request counts  sent as responses 
    2. Top 5 Paths: List of top 5 paths(upto 2 levels) with request counts which recieved maximum number of requests 
    2. Top 5 Response Times: List of top 5 largest response times 
    2. Top 5 Status Codes per Hosts: List of top 5 Status codes with request counts  for each host with the number of requests for each. 
4. Latest Time for status code per host: This tells us what was the last time a particular host sent out a particular status code as a response to a request. (We are only looking at codes 200,4xx and 5xx, rest are filtered out)
5.Requests in last 10 minutes
    1. In the Bash script, this will give us the source IP, Timestamp, Method, Request Path and Protocol version for each request in the last 10 minutes
    2. In the Perl app, this will give us the source IP, Timestamp and Request Path 
    3. In the Python app, this will give us the total number of requests in the last 10 minutes 
6. Requests taking more than 2/5/10 seconds
    Here we get the total counts of requests that take more than 2,5 or 10 seconds to respond. Note the results are not cumulative, i.e if a request takes more than 5 seconds, it is not automatically added to the greater than 2 seconds statistic.


## BASH 
The bash script is called ```stats.sh``` and is in the main directory of the repository. 

It can be downloaded and used by setting the executable bit using 
```
chmod +x stats.sh
```
Next, run the script using the command
```
./stats.sh <path to log file> 
```
Where the path to log file specifies the absolute or relative path to the log file in your file system.

## PERL CGI
To run the perl server, you can use docker to create and configure a container running apache and perl on ubuntu using the docker file in the ```perl-cgi/``` folder. 
### Steps to deploy
1. Switch to the ```perl_cgi``` directory using the following command.
```
cd perl_cgi
```
2. The log file to be processed needs to be uploaded to this folder as the dockerfile needs to upload the file into the container to be able to process it. To copy the file and rename it to the name expected by the application, use the below command.
```
cp <path to log_file> access.log 
```
3. Once the log file is in place, you can start the build using the docker build command as follows
```
docker build -t perl-logstat .  
```
4. Docker will build out the application and create an image. This image can then be used using the following command. Replace the available_local_port_number with a local port number available on the host system, you will ba able to access the perl app on this port from localhost. 
```
sudo docker run -it -p <available_local_port_number>:80/tcp perl-logstat:latest 
```
5. If everything went as expected, you should be dropped into a root prompt for the running container for your image. You can now navigate to ```http://127.0.0.1:<available_local_port_number>/cgi-bin/log-parser.cgi``` to view the statistics from the perl application.