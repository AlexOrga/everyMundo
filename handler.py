import json
import urllib.parse
import boto3
import re
import pandas as pd
import main

s3_client = boto3.client('s3')

# The function definition on line 14 would be used instead of the one on line 15 when used properly as a lambda
# def lambda_handler(event, context):
def lambda_handler():
    # The bucket and Key pair on lines 17 and 18 would be used when properly set up as a lambda
    # these lines automatically pull the most recently added object in the S3 bucket that this lambda
    # is attached to.

    # bucket = event['Records'][0]['s3']['bucket']['name']
    # key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    # These are the bucket name and object name of the file that I used to hold
    # user subscription information. I have these here to pull the files in and test the code
    # below since I was unable to set up a functioning lambda version.
    log_bucket = 'test-lambda-bucket-for-every-mundo'
    log_key = 'logExample'

    try:
        response = s3_client.get_object(Bucket=log_bucket, Key=log_key)

        data = response['Body'].read().decode('utf-8')
        lines = data.splitlines()
        user_subscriptions = get_subscription_details()
        log_statistics = main.get_log_statistics(lines)
        emails_data = build_emails(user_subscriptions, log_statistics)
        for email in emails_data:
            notify(email['email_address'], email['body'])

        return 'Success!'

    except Exception as e:
        print(e)
        raise e


def get_subscription_details():
    user_info_bucket = 'subscriptions-holder'  # Bucket I used to hold the file for user subscription information
    user_info_key = 'test-s3-bucket-v3'        # Object file inside the bucket above that I used to hold user subscription information
    response = s3_client.get_object(Bucket=user_info_bucket, Key=user_info_key)
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
    user_subscriptions_df = pd.DataFrame(user_subscriptions)
    return user_subscriptions_df


def build_emails(user_subscriptions, log_statistics):
    emails_data = []
    unique_email_addresses = user_subscriptions.email.unique()
    for email_address in unique_email_addresses:
        email_body = ''
        filtered_results = user_subscriptions[user_subscriptions["email"] == email_address].sort_values(by=["application", "category"]).reset_index()
        for index, row in filtered_results.iterrows():
            email_body += f'Log Results - Application: {row["application"]} Category: {row["category"]}\n'
            test = main.filter_results(log_statistics, None, row["application"], row["category"], None)
            email_body += f'{test}\n\n'
        emails_data.append({'email_address': email_address, 'body': email_body})
    return emails_data
#
#
def notify(email_address, email_body):
    print(f'To: {email_address}\n {email_body}')


if __name__ == '__main__':
    lambda_handler()
