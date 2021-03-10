from datetime import datetime


def filter_check(time_start, time_end, host, log_line):
    if not time_start and not time_end and not host:
        return True
    elif host and log_line["host"] == host:
        return True
    elif time_start and time_end and (time_start <= log_line['timestamp'] <= time_end):
        return True
    else:
        return False


def read_log(file_path, time_start=None, time_end=None, host=None):
    data = []
    if time_start:
        time_start = datetime.strptime(time_start, "%d/%b/%Y:%H:%M:%S")
    if time_end:
        time_end = datetime.strptime(time_end, "%d/%b/%Y:%H:%M:%S")
    with open(file_path, "r") as f:
        for line in f.readlines():
            log_line_data = {}
            line_arr = line.split()
            log_line_data['source_ip'] = line_arr[0]
            log_line_data['timestamp'] = datetime.strptime(line_arr[1], "%d/%b/%Y:%H:%M:%S")
            log_line_data["method"] = line_arr[3].lstrip('"')
            path_list = line_arr[4].lstrip("/").split("/")
            log_line_data["path"] = "/" + "/".join(path_list[:2]) + "/"
            log_line_data["status_code"] = line_arr[6]
            log_line_data["response_time"] = line_arr[7]
            log_line_data["upstream_ip"] = line_arr[8].split(":")[0]
            log_line_data["upstream_port"] = line_arr[8].split(":")[1]
            log_line_data["bodyBytesSent"] = line_arr[9]
            log_line_data["host"] = line_arr[-1]
            if filter_check(time_start, time_end, host, log_line_data):
                data.append(log_line_data)
    return data
