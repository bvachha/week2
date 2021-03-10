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

## Python Flask Web app
The python flask server introduces some additional functions as compared to the Perl web application. There is a capability to upload '.log' and '.txt' files. We also have the ability to filter on the date range we want as well as the hostname. The details and caveats will be explained below. 

First lets look at setting up the web application
#### Web-server deployment with Docker
1. Navigate to the diectory with the Dockerfile and resources for the python webserver at ```logStatApp``` using the command 
``` 
cd logStatApp 
```
from the root of the project directory.
2. Start the docker build process using 
``` 
docker build -t python-logstat . 
```
This will do the following tasks
    1. Pull an ubuntu base image
    2. Update the apt cache
    2. Install python and pip
    4. Copy over the resource files to the image
    5. Install the python dependencies for the application
    6. Export the applications local port to the host
    7. Setup the initialization command to run the server on container deployment
3. Once the container image is created with no errors, you can use the following command to start the container and bind a host port to the container port. In this example we use port 8080 but it can be any free port on your host system. 
```
sudo docker run -it -p 8080:5000/tcp python-logstat:latest
````
4. Once the container is deployed, you can access the application through the browser on the address ```http://127.0.0.1:8080```
#### Using the web application
* If this is the first time visiting the application after the container is started or restarted, you will see a message asking you to upload a logfile. As there are no additional volumes mounted, the data uploaded will not persist across container reboots. 
* Clicking the upload button will take you to the upload page where you can select a file to upload. The file must be a .txt or a .log file. Any other file types will not be accepted. The format of the logfile should match the below given example format or the parser will not parse the file and return an error message when you try to view the stats page.

```
111.111.111.111 12/Feb/2021:06:52:54 +0000 "GET /xyz/abc/efg/sed HTTP/1.1" 200 0.979 10.11.12.15:443 1407 "-" "User-agent string" TLSv1.2/ECDHE-RSA-AES256-GCM-SHA384 62b5fea87b05d59b-AEN application/json; charset=utf-8 host1.domain.com
```
* where 
    1. 111.111.111.111 is the source IP
    2. 12/Feb/2021:06:52:54 is the date and time information
    3. +0000 is the timezone information
    4. GET is the HTTP Method
    5. /xyz/abc/efg/sed is the request path 
    6. HTTP/1.1 is the http protocol version 
    7.200 is the response status code 
    8. 0.979 is the response time in seconds 
    9. 10.11.12.15:443 is the upstream server and port
    10. 1407 is the size of the response body in bytes
    11. "User-agent string" is the user agent string of the requesting browser
    12. TLSv1.2/ECDHE-RSA-AES256-GCM-SHA384 62b923587b05d59b-BOM is the SSL/TLS information
    13. application/json; charset=utf-8  is the content type
    14. host1.domain.com is the hostname
* Once a properly formatted logfile with the correct extension is uploaded, a new 'View Stats' will appear on the homepage. Clicking this button takes you to the stats page where you can view the various statistics gathered from the logfile. 
* There are two ways to filter information in the statistics:   
    1. _By Hostname:_ If you enter a valid hostname, all the statistics are filtered to only display the statistics for log entries matching that hostname
    2. _By Date Time Range:_ The application accepts a start and end date and filters and processes only those results that are within the specified limits. 
    3. NOTE: Entering invalid hostnames, malformed date ranges or valid ranges with no logs matching them will return a message asking you to check the ranges. If you see this message and are sure your date ranges/hostname data is correct, then it is possible that there is no data matching these values in the log file that was uploaded.
    