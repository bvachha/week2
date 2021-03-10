from datetime import datetime

from logstat.statsParsers.time_stats import get_time_stats, get_requests_last_10_min
from logstat.statsParsers.top_requests_by_resource_type import get_top_requests_by_resource


def get_req_by_stat_code(data):
    result = {}
    for record in data:
        status = str(record.get("status_code"))
        if not result.get(status):
            result[status] = 0
        result[status] += 1
    return sorted(result.items())


def get_latest_time_by_stat_code(data):
    result = {}
    for record in data:
        status = int(record.get("status_code"))
        if not (status == 200 or (400 <= status < 600)):
            continue
        status = str(status)
        host = record["host"]
        time = record.get("timestamp")
        if not result.get(host):
            result[host] = {}
        if not result[host].get(status):
            result[host][status] = time
        if result[host][status] < time:
            result[host][status] = time
    for host in result.keys():
        result[host] = sorted(result[host].items())
    return sorted(result.items())


def get_req_resp_longer_than_intervals(data):
    result = {
        "2 Seconds": 0,
        "5 Seconds": 0,
        "10 Seconds": 0,
    }
    for record in data:
        response_time = float(record["response_time"])
        if 2.0 <= response_time < 5.0:
            result["2 Seconds"] += 1
        elif 5.0 <= response_time < 10.0:
            result["5 Seconds"] += 1
        elif 10.0 <= response_time:
            result["10 Seconds"] += 1
    return result


def get_stats(data):
    stats = {
        "time_stats": get_time_stats(data),
        "total_req_status_code": get_req_by_stat_code(data),
        "top_req_by_resource": get_top_requests_by_resource(data),
        "req_count_last_10_min": get_requests_last_10_min(data),
        "status_code_latest_time": get_latest_time_by_stat_code(data),
        "req_response_longer_than_time_interval": get_req_resp_longer_than_intervals(data)
    }
    return stats
