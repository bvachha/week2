#!/bin/perl -w
use strict;
use CGI;
use HTML::Template;

my $CGI = CGI->new();
print $CGI->header();
my $template = HTML::Template->new(filename => 'logstat.tmpl');
my $log_path = "~/access.log";


sub daily_summary_host {
	my $command = q(awk -F'[ :]' '{print $2,$NF }' | sort -k 1.8,1.11n -k 1.4,1.6M -k 1.1,1.2n | uniq -c | sort -k 2.9,2.12n -k 2.5,2.7M -k 2.1,2.3n -k 1,1rn | uniq --skip-fields=1 --check-chars=10 |awk '{printf "%-20s\t%-20s\t%-10d\n",$2,$3,$1}');
	my $data = `cat $log_path | $command`;
	my @rows = split("\n",$data);
	my $template_data;
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			DATE => $split_row[0],
			HOST => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(DAILY_HOST => $template_data);
}

sub daily_summary_path {
	my $command = q(awk -F'[ :]' '{print $2,$8 }' | sed -E 's/(\/[[:alpha:]]{3}\/[[:digit:]]{4} \/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' | sort -k 1.8,1.11n -k 1.4,1.6M -k 1.1,1.2n | uniq -c | sort -k 2.9,2.12n -k 2.5,2.7M -k 2.1,2.3n -k 1,1rn | uniq --skip-fields=1 --check-chars=10 | awk '{printf "%s\t%s\t%s\n", $2,$3,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			DATE => $split_row[0],
			PATH => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(DAILY_PATH => $template_data);
}

sub daily_summary_upstream_ip {
	my $command = q(awk -F'[ :]' '{print $2,$12 }' | sort -k 1.8,1.11n -k 1.4,1.6M -k 1.1,1.2n | uniq -c | sort -k 2.9,2.12n -k 2.5,2.7M -k 2.1,2.3n -k 1,1rn | uniq --skip-fields=1 --check-chars=10 |awk '{printf "%-20s\t%-20s\t%-10d\n",$2,$3,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			DATE => $split_row[0],
			UPSTREAM_IP => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(DAILY_UPSTREAM_IP => $template_data);
}

sub get_daily_stats {
	daily_summary_host();
	daily_summary_upstream_ip();
	daily_summary_path();
}

sub weekly_summary_host {
	my $command = q(awk -F'[ :]' '{print $2,$NF }' |sed -e 's/\//-/g' | awk '{ record_date = "date --date="$1" -u +%V" 
		record_date | getline log_date 
		print  log_date, $2 }' | sort -k2n |uniq -c | sort -k2n -k1nr | awk '{if (week_number<$2) {printf "%-10d\t%-20s\t%-10d\n",$2,$3,$1; week_number=$2}}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			WEEK => $split_row[0],
			HOST => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(WEEKLY_HOST => $template_data);
}

sub weekly_summary_upstream_ip {
	my $command = q(awk -F'[ :]' '{print $2,$12 }' |sed -e 's/\//-/g' | awk '{ record_date = "date --date="$1" -u +%V" 
		record_date | getline log_date 
		print  log_date, $2 }' | sort -k2n |uniq -c | sort -k2n -k1nr | awk '{if (week_number<$2) {printf "%-10d\t%-20s\t%-10d\n",$2,$3,$1; week_number=$2}}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			WEEK => $split_row[0],
			UPSTREAM_IP => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(WEEKLY_UPSTREAM => $template_data);
}

sub weekly_summary_path {
	my $command = q(awk -F'[ :]' '{print $2,$8 }' | sed -e 's/\//-/' -e 's/\//-/' | sed -E 's/( \/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' | awk '{ 
 	record_date = "date --date="$1" -u +%V"
 	record_date | getline log_date
  	print  log_date, $2
  }' | sort -k2n |uniq -c | sort -k2n -k1nr | awk '{
	if (week_number<$2) {
		printf "%-10d\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			WEEK => $split_row[0],
			PATH => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(WEEKLY_PATH => $template_data);
}

sub get_weekly_stats {
	weekly_summary_host();
	weekly_summary_upstream_ip();
	weekly_summary_path();
}

sub monthly_summary_host {
	my $command = q(awk -F'[ :]' '{print $2,$NF }' |sed -e 's/\//-/g' | awk '{ 
		record_date = "date --date="$1" -u +%b"
	 	record_date | getline log_date
	  	print  log_date, $2
  	}' | sort -k2,2M | uniq -c | sort -k2,2M -k1nr | awk '{
	if (week_number!=$2) {
		printf "%-10s\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			MONTH => $split_row[0],
			HOST => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(MONTHLY_HOST => $template_data);
}

sub monthly_summary_upstream_ip {
	my $command = q(awk -F'[ :]' '{print $2,$12 }' |sed -e 's/\//-/g' | awk '{ 
		record_date = "date --date="$1" -u +%b"
	 	record_date | getline log_date
	  	print  log_date, $2
  	}' | sort -k2,2M | uniq -c | sort -k2,2M -k1nr | awk '{
	if (week_number!=$2) {
		printf "%-10s\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			MONTH => $split_row[0],
			UPSTREAM_IP => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(MONTHLY_UPSTREAM_IP => $template_data);
}

sub monthly_summary_path {
	my $command = q(awk -F'[ :]' '{print $2,$8 }' | sed -e 's/\//-/' -e 's/\//-/' | sed -E 's/( \/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' | awk '{ 
 	record_date = "date --date="$1" -u +%b"
 	record_date | getline log_date
  	print  log_date, $2
  }' |sort -k2,2M |uniq -c |sort -k2,2M -k1nr |awk '{
	if (week_number!=$2) {
		printf "%-10s\t%-20s\t%-10d\n",$2,$3,$1;
	    week_number=$2
	}}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			MONTH => $split_row[0],
			PATH => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(MONTHLY_PATH => $template_data);
}

sub get_monthly_stats {
	monthly_summary_host();
	monthly_summary_upstream_ip();
	monthly_summary_path();
}

sub get_total_request_by_status_code{
	my $command = q(awk '{ print $7}' | tr --delete '"' | sort | uniq -c | awk '{printf "%d\t%d \n", $2,$1}'
);
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			STATUS_CODE => $split_row[0],
			REQCOUNT => $split_row[1]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TOTAL_REQ_BY_STATUS => $template_data);
}

sub top_5_upstream{
	my $command = q(awk -F"[ :]" '{print $12}' | sort | uniq -c | sort -k1rn | head -n5 | awk '{printf "%-30s\t%-10d\n",$2,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			UPSTREAM_IP => $split_row[0],
			REQCOUNT => $split_row[1]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TOP_5_UPSTREAM => $template_data);
}

sub top_5_host{
	my $command = q(awk -F"[ :]" '{print $NF}' | sort | uniq -c | sort -k1rn | head -n5 | awk '{printf "%-30s\t%-10d\n",$2,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			HOST => $split_row[0],
			REQCOUNT => $split_row[1]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TOP_5_HOST => $template_data);
}

sub top_5_body_bytes{
	my $command = q(awk -F"[ :]" '{print $14}' | sort | uniq -c | sort -k1rn | head -n5 | awk '{printf "%-30s\t%-10d\n",$2,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			BODY_BYTES => $split_row[0],
			REQCOUNT => $split_row[1]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TOP_5_BODYBYTES => $template_data);
}

sub top_5_path{
	my $command = q(awk -F'[ :]' '{print $8 }' | sed -E 's/(\/[[:alnum:]]*\/[[:alnum:]]*\/)(.*)/\1/' | sort | uniq -c | sort -k1r | head -n5 | awk '{printf "%-20s\t%-10d\n",$2,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			PATH => $split_row[0],
			REQCOUNT => $split_row[1]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TOP_5_PATH => $template_data);
}

sub top_5_response_times{
	my $command = q(awk -F'[ :]' '{print $11 }' | sort -nr | uniq -c | head -n5 | awk '{printf "%-20s\t%-10d\n",$2,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			RESP_TIME => $split_row[0],
			REQCOUNT => $split_row[1]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TOP_5_RESP_TIME => $template_data);
}

sub top_5_status_by_host{
	my $command = q(awk -F"[ :]" '{if(($10==200) ||($10>=400 && $10<600)) print $10,$NF}' | sort -k2 | uniq -c | sort -k3 -k1nr | awk 'BEGIN{counter = 0; host="";}{ if (host!=$3) {print $0; counter=1;host=$3;} else if (host==$3 && counter<5) {print $0; counter = counter+1;}}'| awk '{printf "%-20s\t%-10d\t%-10d\n",$3,$2,$1}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			HOST => $split_row[0],
			STATUS => $split_row[1],
			REQCOUNT => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TOP_5_STATUS_BY_HOST => $template_data);
}


sub get_top_requests {
	top_5_upstream();
	top_5_host();
	top_5_body_bytes();
	top_5_path();
	top_5_response_times();
	top_5_status_by_host();
}

sub latest_time_status_by_host{
	my $command = q(awk -F'[: ]' '{if($10==200 || ($10>=400 && $10<600)) print $2,$3,$4,$5,$10,$NF}' | sort -k6,6 -k5,5 -k1.8,1.11nr -k1.4,1.6Mr -k 1.1,1.2rn -k2,2rn -k3,3nr -k4,4nr | uniq -c --skip-fields=4 | awk ' {printf "%-20s\t%-10d\t%s:%s:%s:%s\n",$7,$6,$2,$3,$4,$5}');
	my $data = `cat $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			HOST => $split_row[0],
			STATUS => $split_row[1],
			TIME => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(TIME_STATUS_HOST => $template_data);
}

sub req_last_10_mins{
	my $last_time_extractor = q(awk '{print $2}' | sed -e 's/:/ /' -e 's/\//-/g' | xargs -I {} date --date='{}' -u);
	my $last_entry =`tail $log_path -n1 | $last_time_extractor`;
	my $start_time = `date --date="$last_entry -10 minutes" -u +%s`;
	chomp($start_time);
	my $command = q(awk -v start=$start_time '{ 
	record_date = "echo "$2" | sed -e \"s/:/ /\" -e \"s/\//-/g\"  | xargs -I {} date --date={} -u +%s"
	record_date | getline log_date 
	if (log_date >= start)
		print $1,$2,$5;
	else
		exit 0}' );
	my $data = `start_time=$start_time && tac $log_path | $command`;
	my $template_data;
	my @rows = split("\n",$data);
	foreach my $row (@rows){
		my @split_row = split(" ",$row);
		my $parsed_row = {
			IP => $split_row[0],
			TIME => $split_row[1],
			REQ => $split_row[2]
		};
		push @{$template_data}, $parsed_row;
	}
	$template -> param(REQ_LAST_10_MIN => $template_data);
}

sub req_by_resp_intervals{
	my $command = q(awk -F"[ :]" '{print $11}' | sort -n | uniq -c | awk 'BEGIN {time[2]=0; time[5]=0;time[10]=0} { if ($2>=2.0 && $2<5.0) time[2]+=$1; else if ($2>=5.0 && $2<10.0)	time[5] +=$1;else if ($2 >=10.0) time[10] += $1 ;} END{printf "%d\t%d\t%d",time[2],time[5],time[10]}');
	my $data = `cat $log_path | $command`;
	my @split_row = split(" ",$data);
	$template -> param(gt2 => $split_row[0],gt5 => $split_row[1],gt10 => $split_row[2],);
}


sub main {
	get_daily_stats();
	get_weekly_stats();
	get_monthly_stats();
	get_total_request_by_status_code();
	get_top_requests();
	latest_time_status_by_host();
	req_last_10_mins();
	req_by_resp_intervals();	
	print $template->output();
}

main();