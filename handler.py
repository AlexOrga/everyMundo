import json
import boto3
import re
# import pandas as pd

import main

s3_client = boto3.client('s3')
S3_BUCKET_NAME = 'test-lambda-bucket-for-every-mundo'

def get_subscription_details(event, context):
# def get_subscription_details():
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key='test-s3-bucket-v2')
    contents = response['Body'].read().decode('utf-8')
    matches = re.findall(r"(.*@.*)\s-\s(\w+)\s-\s(\w+)\n", contents)

    user_subscriptions = []
    for match in matches:
        log_details = {
            'email': match[0].strip(),
            'application': match[1].strip(),
            'category': match[2].strip()
        }
        user_subscriptions.append(log_details)
    logs = get_logs()
    #
    # user_subscriptions_df = pd.DataFrame(user_subscriptions)
    # message = build_email(user_subscriptions_df)

    body = {
        "message": logs,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def get_logs():
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key='logExample')
    return response
    # contents = response['Body'].read().decode('utf-8')
    # lines = contents.splitlines()
    # log_statistics = main.get_log_statistics(lines)
    # return log_statistics
#
#
# def build_email(user_subscriptions):
#     full_message = ''
#     unique_email_addresses = user_subscriptions.email.unique()
#     log_stats = get_logs()
#     for email_address in unique_email_addresses:
#         email_body = ''
#         filtered_results = user_subscriptions[user_subscriptions["email"] == email_address].sort_values(by=["application", "category"]).reset_index()
#         for index, row in filtered_results.iterrows():
#             email_body += f'Log Results - Application: {row["application"]} Category: {row["category"]}\n'
#             test = main.filter_results(log_stats, None, row["application"], row["category"], None)
#             email_body += f'{test}\n\n'
#         full_message += notify(email_address, email_body)
#     return full_message
#
#
# def notify(email_address, email_body):
#     return f'To: {email_address}\n {email_body}'


if __name__ == '__main__':
    get_subscription_details()

# def notify(email, content):
