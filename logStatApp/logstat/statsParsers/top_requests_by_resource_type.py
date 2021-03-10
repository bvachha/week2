def top_requests_by_field(data, field):
    result = {}
    for record in data:
        if not result.get(record[field]):
            result[record[field]] = 0
        result[record[field]] += 1
    if field != "response_time":
        return sorted(result.items(), key=lambda k: k[1], reverse=True)[0:5]
    else:
        return sorted(result.items(), key=lambda k: float(k[0]), reverse=True)[0:5]


def top_req_codes_by_host(data):
    result = {}
    for record in data:
        host = record["host"]
        status_code = int(record["status_code"])
        if not (status_code == 200 or (400 <= status_code < 600)):
            continue
        status_code = str(status_code)
        if not result.get(host):
            result[host] = {}
        if not result[host].get(status_code):
            result[host][status_code] = 0
        result[host][status_code] += 1
    for host in result.keys():
        result[host] = sorted(result[host].items(), key=lambda k: k[1], reverse=True)[0:5]
    return result


def get_top_requests_by_resource(data):
    result = {}
    resource_list = ['upstream_ip', 'host', 'bodyBytesSent', 'path', 'response_time']
    for resource in resource_list:
        result[resource] = top_requests_by_field(data, resource)
    result["code_by_host"] = top_req_codes_by_host(data)
    return result
