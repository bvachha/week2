#Setup base Image 
FROM ubuntu:latest

# Set correct environment variables.
ENV HOME /root

# Update the apt cache
RUN apt-get update

#Install the webserver
RUN DEBIAN_FRONTEND="noninteractive" apt-get install --yes apache2
# Install dependencies, perl and CPAN
RUN apt-get install -y build-essential
RUN apt-get install --yes perl

# Install the required perl modules from CPAN
RUN perl -MCPAN -e "install CGI"
RUN perl -MCPAN -e "install HTML::Template"

#Enable the apache module for CGI and restart the server to let changes take effect
RUN a2enmod cgid
RUN service apache2 restart

#Switch the working dir to the default cgi dir
WORKDIR /usr/lib/cgi-bin

#Copy over the required cgi, template and data files to the correct locations in the container filesystem 
COPY log-parser.cgi .
COPY logstat.tmpl .
COPY access.log ~/

# Set the correct permissions for the files in the cgi-bin folder
RUN chmod 755 log-parser.cgi
RUN chmod 755 logstat.tmpl

# Expose the local port to docker 
EXPOSE 80/TCP

# Setup a command to start the apache server on container deployment 
CMD service apache2 start && bash 