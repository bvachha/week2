from datetime import datetime
from typing import List, Dict


def get_time_intervals(data):
    """
    gets the unique date, week and months from the data records
    :param data: log data
    :return: unique dates, week numbers and month names present in the logs
    """
    dates = list(set(record['timestamp'].date() for record in data))
    weeks = list(set(record['timestamp'].date().isocalendar()[1] for record in data))
    months = list(set(record['timestamp'].strftime("%b") for record in data))
    return dates, weeks, months


def get_daily_stats(dates: List[datetime], data: List[Dict]):
    """
    gets the top host, path and upstream ip address for a given date
    :param dates: list of date values
    :param data: list of log records
    :return: date wise stats for each specified resource type
    """
    stats_data = {}
    for record in data:
        for date in dates:
            if record['timestamp'].date() == date:
                if not stats_data.get(str(date)):
                    stats_data[str(date)] = {
                        'host_counts': {},
                        'upstream_ip_counts': {},
                        'path_counts': {}
                    }
                if not stats_data.get(str(date)).get("host_counts").get(record['host']):
                    stats_data[str(date)]["host_counts"][record['host']] = 0
                if not stats_data.get(str(date)).get("upstream_ip_counts").get(record['upstream_ip']):
                    stats_data[str(date)]["upstream_ip_counts"][record['upstream_ip']] = 0
                if not stats_data.get(str(date)).get("path_counts").get(record['path']):
                    stats_data[str(date)]["path_counts"][record['path']] = 0
                stats_data[str(date)]["host_counts"][record['host']] += 1
                stats_data[str(date)]["upstream_ip_counts"][record['upstream_ip']] += 1
                stats_data[str(date)]["path_counts"][record['path']] += 1
    final_data = aggregate_time_stats(stats_data)
    return final_data


def aggregate_time_stats(stats_data):
    """
    aggregate the data and generate a new list of values with key as the resource and value being the time interval
    and resource name
    :param stats_data: stats data extracted
    :return:aggregated time stats
    """
    final_data = {
        "hosts": [],
        "upstream_ip": [],
        "path": []
    }
    for key in stats_data.keys():
        host_counts = stats_data[key]['host_counts']
        max_host_key = max(host_counts, key=host_counts.get)
        upstream_ip_counts = stats_data[key]['upstream_ip_counts']
        max_upstream_key = max(upstream_ip_counts, key=upstream_ip_counts.get)
        path_counts = stats_data[key]['path_counts']
        max_path_counts = max(path_counts, key=path_counts.get)
        final_data["hosts"].append({
            "time_interval": key,
            "host": max_host_key,
            "requests": host_counts[max_host_key]
        })
        final_data["upstream_ip"].append({
            "time_interval": key,
            "upstream_ip": max_upstream_key,
            "requests": upstream_ip_counts[max_upstream_key]
        })
        final_data["path"].append({
            "time_interval": key,
            "path": max_path_counts,
            "requests": path_counts[max_path_counts]
        })
    return final_data


def get_weekly_stats(weeks, data):
    """
        gets the top host, path and upstream ip address for a given week number
        :param weeks: list of week number values
        :param data: list of log records
        :return: date wise stats for each specified resource type
        """
    stats_data = {}
    for record in data:
        for week_num in weeks:
            week_num = str(week_num)
            if record['timestamp'].date().isocalendar()[1] == int(week_num):
                if not stats_data.get(week_num):
                    stats_data[str(week_num)] = {
                        'host_counts': {},
                        'upstream_ip_counts': {},
                        'path_counts': {}
                    }
                if not stats_data.get(week_num).get("host_counts").get(record['host']):
                    stats_data[week_num]["host_counts"][record['host']] = 0
                if not stats_data.get(week_num).get("upstream_ip_counts").get(record['upstream_ip']):
                    stats_data[week_num]["upstream_ip_counts"][record['upstream_ip']] = 0
                if not stats_data.get(week_num).get("path_counts").get(record['path']):
                    stats_data[week_num]["path_counts"][record['path']] = 0
                stats_data[week_num]["host_counts"][record['host']] += 1
                stats_data[week_num]["upstream_ip_counts"][record['upstream_ip']] += 1
                stats_data[week_num]["path_counts"][record['path']] += 1
    final_data = aggregate_time_stats(stats_data)
    return final_data


def get_monthly_stats(months, data):
    """
        gets the top host, path and upstream ip address for a given month
        :param months: list of month values
        :param data: list of log records
        :return: date wise stats for each specified resource type
        """
    stats_data = {}
    for record in data:
        for month in months:
            if record['timestamp'].date().strftime('%b') == month:
                if not stats_data.get(month):
                    stats_data[str(month)] = {
                        'host_counts': {},
                        'upstream_ip_counts': {},
                        'path_counts': {}
                    }
                if not stats_data.get(month).get("host_counts").get(record['host']):
                    stats_data[month]["host_counts"][record['host']] = 0
                if not stats_data.get(month).get("upstream_ip_counts").get(record['upstream_ip']):
                    stats_data[month]["upstream_ip_counts"][record['upstream_ip']] = 0
                if not stats_data.get(month).get("path_counts").get(record['path']):
                    stats_data[month]["path_counts"][record['path']] = 0
                stats_data[month]["host_counts"][record['host']] += 1
                stats_data[month]["upstream_ip_counts"][record['upstream_ip']] += 1
                stats_data[month]["path_counts"][record['path']] += 1
    final_data = aggregate_time_stats(stats_data)
    return final_data


def get_requests_last_10_min(data):
    """
        gets the count of total requests received for the last 10 minutes
        :param data: list of log records
        :return: count of received requests for last 10 minutes
        """
    counter = 0
    last_entry_time = data[-1]['timestamp']
    for record in data:
        difference = last_entry_time - record['timestamp']
        if (difference.total_seconds() / 60) <= 10:
            counter += 1
    return counter


def get_time_stats(data):
    """
    generates the time based statistics groups
    :param data: log data
    :return: dict of time based stats
    """
    dates, weeks, months = get_time_intervals(data)
    return {
        'daily_stats': get_daily_stats(dates, data),
        'weekly_stats': get_weekly_stats(weeks, data),
        'monthly_stats': get_monthly_stats(months, data)
    }
