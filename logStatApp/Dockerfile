#Setup base Image 
FROM ubuntu:latest

# Set correct environment variables.
ENV HOME /root
WORKDIR /root/
ENV FLASK_APP=logstat.py
ENV FLASK_ENV=production

# Update the apt cache
RUN apt-get update

# Install python and pip dependencies 
RUN apt install -y python3 python3-pip

# copy files to the container image
COPY ./logstat /root/logstat/
COPY config.py /root/
COPY requirements.txt /root/
COPY logstat.py /root/

# Get the requirements for the flask app
RUN pip3 install -r requirements.txt

# Expose the application port to host
EXPOSE 5000/tcp

# command to initialise container
CMD bash -c '(flask run --host "0.0.0.0"&) && bash'