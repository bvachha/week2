#! /bin/bash 
#######################################################################################
# Bash file to extract statistics from nginx logs 
# Requires a path to nginx log file as the first and only parameter to the script
######################################################################################

if [ $# -eq 0 ]
then
	echo "Please provide a path to the log file as an argument"
	exit 1
fi

echo "================================================================="
echo "Statistics by Day"
echo "-----------------------------------------------------------------"
echo "Highest requested host per Day"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$NF }' \
| sort -k 1.8,1.11n -k 1.4,1.6M -k 1.1,1.2n \
| uniq -c \
| sort -k 2.9,2.12n -k 2.5,2.7M -k 2.1,2.3n -k 1,1rn \
| uniq --skip-fields=1 --check-chars=10 \
|awk 'BEGIN {printf "%-20s\t%-20s\t%-10s\n","Date","Host","Requests"} {printf "%-20s\t%-20s\t%-10d\n",$2,$3,$1}'

echo "-----------------------------------------------------------------"
echo "Highest requested Upstream IP per Day"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$12 }' \
| sort -k 1.8,1.11n -k 1.4,1.6M -k 1.1,1.2n \
| uniq -c \
| sort -k 2.9,2.12n -k 2.5,2.7M -k 2.1,2.3n -k 1,1rn \
| uniq --skip-fields=1 --check-chars=10 \
|awk 'BEGIN {printf "%-20s\t%-20s\t%-10s\n","Date","IP","Requests"} {printf "%-20s\t%-20s\t%-10d\n",$2,$3,$1}'

echo "-----------------------------------------------------------------"
echo "Highest requested Path per Day"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$8 }' \
| sed -E 's/(\/[[:alpha:]]{3}\/[[:digit:]]{4} \/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' \
| sort -k 1.8,1.11n -k 1.4,1.6M -k 1.1,1.2n \
| uniq -c \
| sort -k 2.9,2.12n -k 2.5,2.7M -k 2.1,2.3n -k 1,1rn \
| uniq --skip-fields=1 --check-chars=10  \
| awk 'BEGIN {printf "%-10s\t%-30s\t%-10s\n","Date","Path","Requests"} {printf "%-10s\t%-30s\t%-10s\n", $2,$3,$1}'


echo "================================================================="
echo "Statistics by Week"
echo "-----------------------------------------------------------------"
echo "Highest requested host per Week"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$NF }' \
|sed -e 's/\//-/g' \
| awk '{ 
 	record_date = "date --date="$1" -u +%V"
 	record_date | getline log_date
  	print  log_date, $2
  }' \
| sort -k2n \
|uniq -c \
| sort -k2n -k1nr \
| awk 'BEGIN {
	printf "%-10s\t%-20s\t%-10s\n","Week Number","Host","Request Count"
}
{
	if (week_number<$2) {
		printf "%-10d\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}
}'

echo "-----------------------------------------------------------------"
echo "Highest requested Upstream IP per Week"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$12 }' \
|sed -e 's/\//-/g' \
| awk '{ 
 	record_date = "date --date="$1" -u +%V"
 	record_date | getline log_date
  	print  log_date, $2
  }' \
| sort -k2n \
|uniq -c \
| sort -k2n -k1nr \
| awk 'BEGIN {
	printf "%-10s\t%-20s\t%-10s\n","Week Number","Upstream IP","Request Count"
}
{
	if (week_number<$2) {
		printf "%-10d\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}
}'

echo "-----------------------------------------------------------------"
echo "Highest requested Path per Week"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$8 }' \
| sed -e 's/\//-/' -e 's/\//-/' \
| sed -E 's/( \/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' \
| awk '{ 
 	record_date = "date --date="$1" -u +%V"
 	record_date | getline log_date
  	print  log_date, $2
  }' \
| sort -k2n \
|uniq -c \
| sort -k2n -k1nr \
| awk 'BEGIN {
	printf "%-10s\t%-20s\t%-10s\n","Week Number","Path","Request Count"
}
{
	if (week_number<$2) {
		printf "%-10d\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}
}'


echo "================================================================="
echo "Statistics by Month"
echo "-----------------------------------------------------------------"
echo "Highest requested host per Month"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$NF }' \
|sed -e 's/\//-/g' \
| awk '{ 
 	record_date = "date --date="$1" -u +%b"
 	record_date | getline log_date
  	print  log_date, $2
  }' \
| sort -k2,2M \
|uniq -c \
| sort -k2,2M -k1nr \
| awk 'BEGIN {
	printf "%-10s\t%-20s\t%-10s\n","Month","Host","Request Count"
}
{
	if (week_number!=$2) {
		printf "%-10s\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}
}'

echo "-----------------------------------------------------------------"
echo "Highest requested Upstream IP per Month"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$12 }' \
|sed -e 's/\//-/g' \
| awk '{ 
 	record_date = "date --date="$1" -u +%b"
 	record_date | getline log_date
  	print  log_date, $2
  }' \
| sort -k2,2M \
|uniq -c \
| sort -k2,2M -k1nr \
| awk 'BEGIN {
	printf "%-10s\t%-20s\t%-10s\n","Month","IP","Request Count"
}
{
	if (week_number!=$2) {
		printf "%-10s\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}
}'

echo "-----------------------------------------------------------------"
echo "Highest requested Path per Month"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $2,$8 }' \
| sed -e 's/\//-/' -e 's/\//-/' \
| sed -E 's/( \/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' \
| awk '{ 
 	record_date = "date --date="$1" -u +%b"
 	record_date | getline log_date
  	print  log_date, $2
  }' \
|sort -k2,2M \
|uniq -c \
|sort -k2,2M -k1nr \
|awk 'BEGIN {
	printf "%-10s\t%-20s\t%-10s\n","Month","Path","Request Count"
}
{
	if (week_number!=$2) {
		printf "%-10s\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}
}'


echo "================================================================="
echo "Status code Statistics "
echo "================================================================="
echo "-----------------------------------------------------------------"
echo "Total Requests by status code"
echo "-----------------------------------------------------------------"
echo ""
cat $1 \
|  awk '{ print $7}' \
| tr --delete '"' \
| sort \
| uniq -c \
| awk 'BEGIN {printf "%-10s\t%-10s\n","Status code","Requests"} {printf "%-10d\t%-10d \n", $2,$1}'

echo "================================================================="
echo "Top Requests"
echo "-----------------------------------------------------------------"
echo "Top 5 upstream IPs"
echo "-----------------------------------------------------------------"
echo ""
echo 
cat $1 |awk -F"[ :]" '{print $12}' \
| sort \
| uniq -c \
| sort -k1rn \
| head -n5 \
| awk 'BEGIN {printf "%-30s\t%-10s\n","Upstream IP","Requests"} {printf "%-30s\t%-10d\n",$2,$1}'

echo "-----------------------------------------------------------------"
echo "Top 5 hosts"
echo "-----------------------------------------------------------------"
echo ""
cat $1 |awk -F"[ :]" '{print $NF}' \
| sort \
| uniq -c \
| sort -k1rn \
| head -n5 \
| awk 'BEGIN {printf "%-30s\t%-10s\n","Host","Requests"} {printf "%-30s\t%-10d\n",$2,$1}'

echo "-----------------------------------------------------------------"
echo "Top 5 Body bytes sent"
echo "-----------------------------------------------------------------"
echo ""
cat $1 |awk -F"[ :]" '{print $14}' \
| sort \
| uniq -c \
| sort -k1rn \
| head -n5 \
| awk 'BEGIN {printf "%-10s\t%-10s\n","Bytes Sent","Requests"} {printf "%-10s\t%-10d\n",$2,$1}'

echo "-----------------------------------------------------------------"
echo "Top 5 Paths"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $8 }' \
| sed -E 's/(\/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' \
| sort \
| uniq -c \
| sort -k1r \
| head -n5 \
| awk 'BEGIN {printf "%-20s\t%-10s\n","Path","Requests"} {printf "%-20s\t%-10d\n",$2,$1}'

echo "-----------------------------------------------------------------"
echo "Top 5 Highest Response Times"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[ :]' '{print $11 }' \
| sort -nr \
| uniq -c \
| head -n5 \
| awk 'BEGIN {printf "%-20s\t%-10s\n","Response Time","Requests"} {printf "%-20s\t%-10d\n",$2,$1}'


echo "-----------------------------------------------------------------"
echo "Top 5 Response codes by host"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F"[ :]" '{if(($10==200) ||($10>=400 && $10<600)) print $10,$NF}' \
| sort -k2 \
| uniq -c \
| sort -k3 -k1nr \
| awk 'BEGIN{counter = 0; host="";}{ if (host!=$3) {print $0; counter=1;host=$3;} else if (host==$3 && counter<5) {print $0; counter = counter+1;}}' \
| awk 'BEGIN {printf "%-20s\t%-10s\t%-30s\n","Host", "Status Code", "Requests"} {printf "%-20s\t%-10d\t%-10d\n",$3,$2,$1}'



echo "-----------------------------------------------------------------"
echo "Host-wise latest time per status code"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F'[: ]' '{if($10==200 || ($10>=400 && $10<600)) print $2,$3,$4,$5,$10,$NF}' \
| sort -k6,6 -k5,5 -k1.8,1.11nr -k1.4,1.6Mr -k 1.1,1.2rn -k2,2rn -k3,3nr -k4,4nr \
| uniq -c --skip-fields=4 \
| awk 'BEGIN {printf "%-20s\t%-10s\t%-30s\n","Host", "Status Code", "Time"} {printf "%-20s\t%-10d\t%s:%s:%s:%s\n",$7,$6,$2,$3,$4,$5}'


echo "-----------------------------------------------------------------"
echo "Requests for last 10 minutes"
echo "-----------------------------------------------------------------"
echo ""
last_entry=$(tail access.log -n1 | awk '{print $2}' | sed -e 's/:/ /' -e 's/\//-/g' | xargs -I {} date --date='{}' -u)
start_time=$( date --date="$last_entry -10 minutes" -u +%s)
tac $1 \
|awk -v start=$start_time '{ 
	record_date = "echo "$2" | sed -e \"s/:/ /\" -e \"s/\//-/g\"  | xargs -I {} date --date={} -u +%s"
	record_date | getline log_date 
	if (log_date >= start)
		print $1,$2,$4,$5,$6;
	else
		exit 0
}' 



echo "-----------------------------------------------------------------"
echo "Requests response statistics"
echo "-----------------------------------------------------------------"
echo ""
cat $1 | awk -F"[ :]" '{print $11}' \
| sort -n \
| uniq -c \
| awk 'BEGIN { printf "%-30s\t%-30s\t%-30s\n","Requests response > 2s","Requests response > 5s","Requests response > 10s";time[2]=0; time[5]=0;time[10]=0} { if ($2>=2.0 && $2<5.0) time[2]+=$1; else if ($2>=5.0 && $2<10.0)	time[5] +=$1;else if ($2 >=10.0) time[10] += $1 ;} END{printf "%-30d\t%-30d\t%-30d\n",time[2],time[5],time[10]}'