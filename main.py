#/Users/alexanderorga/.pyenv/shims/python
from argparse import ArgumentParser
import re
import pandas as pd

def do_all(file_path, timestamp_filter, application_filter, category_filter, severity_filter):
    log_results = get_log_statistics_from_file_path(file_path)

    print_counts(log_results)

    filtered_results = filter_results(log_results, timestamp_filter, application_filter, category_filter, severity_filter)
    print(filtered_results)


#Exercise 1
def print_counts(log_results):
    print(f'Error Count: {log_results[log_results["category"].str.lower() == "error"].shape[0]}')
    print(f'Success Count: {log_results[log_results["category"].str.lower() == "success"].shape[0]}')
    print(f'Total Count: {log_results.shape[0]}')


#Exercise 2
def filter_results(log_results, timestamp_filter, application_filter, category_filter, severity_filter):
    filtered_results = log_results
    if timestamp_filter is not None:
        filtered_results = filtered_results[filtered_results["timestamp"].str.lower() == timestamp_filter.lower()]
    if application_filter is not None:
        filtered_results = filtered_results[filtered_results["application"].str.lower() == application_filter.lower()]
    if category_filter is not None:
        filtered_results = filtered_results[filtered_results["category"].str.lower() == category_filter.lower()]
    if severity_filter is not None:
        filtered_results = filtered_results[filtered_results["severity"].str.lower() == severity_filter.lower()]


    if filtered_results.shape[0] != 0:
        return filtered_results.sort_values(by=["timestamp"]).reset_index(drop=True)
    else:
        return 'No Results Matching Your Filters.'


def get_log_statistics_from_file_path(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        all_logs = get_log_statistics(lines)

        all_logs_df = pd.DataFrame(all_logs)
        f.close()
    return all_logs_df


def get_log_statistics(log_lines):
    data = (' ').join([line.strip() for line in log_lines if line.strip()])
    data = re.sub("(\d+T\d+:\d+)", "\n \\1", data)
    matches = re.findall(r"(\d+T\d+:\d+)\s-\s(\w+)\s-\s(\w+)(\s\[\d\])*:(.*)", data)

    all_logs = []
    for match in matches:
        log_details = {
            'timestamp': match[0].strip(),
            'application': match[1].strip(),
            'category': match[2].strip(),
            'severity': re.sub(r"\[(\d)\]", "\\1", match[3]).strip(),
            'message': match[4].strip()
        }
        all_logs.append(log_details)

    all_logs_df = pd.DataFrame(all_logs)

    return all_logs_df


if __name__ == '__main__':
    arg_parser = ArgumentParser(description='Obtain statistics from a log file.')
    arg_parser.add_argument('-f', '--file-path', help='Full path to the log file that needs to be read')
    arg_parser.add_argument('-t', '--timestamp-filter', default=None, help='Timestamp that you want to filter by')
    arg_parser.add_argument('-a', '--application-filter', default=None, help='Application name that you want to filter by: APP, SERVER, etc.')
    arg_parser.add_argument('-c', '--category-filter', default=None, help='Category that you want to filter by: SUCCESS, ERROR, INFO, etc.')
    arg_parser.add_argument('-s', '--severity-filter', default=None, help='Numerical value of the severity level you want to filter by: 1-5')

    args = arg_parser.parse_args()

    do_all(args.file_path, args.timestamp_filter, args.application_filter, args.category_filter, args.severity_filter)


