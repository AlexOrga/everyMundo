<h1>Alex Orga Code Exercise EveryMundo</h1>

<h3>There are 2 main uses for this project:</h3>

The ability to gain statistics about logging events when passing in a log file. Returning overall counts of events as well as detailed event information that is filterable.

The ability to pull a log file from an AWS S3 bucket. The ability to pull a file from another AWS S3 bucket filled with user email and subscription information. Filtering log events based on user subscription and then returning an object with the user's email address and an email body containing only the log information they are subscribed to.

<h3>Technologies used</h3>
- Python3.9
- Pandas
- boto3

I used Pandas on this project because I really love how easy pandas DataFrames are to work with. Being able to quickly turn objects into a tabular data structure not only feels more organized but it makes grouping like-values so much easier.

<h3>Challenges and Future Features:</h3>

Challenges I incurred were centered completely around the AWS Lambda implementation. Since I am choosing to use Pandas, and Pandas is not natively available for import on AWS, I needed to find a way to package the Pandas module and send it to AWS. I first attempted this through the serverless framework and eventually attempted just loading a zip file as an S3 object and tried attaching the layer to my lambda function via the AWS console. I was continuously met with an error stating Function code combined with layers exceeds the maximum allowed size and was unable to remedy this issue.

I would like to be able to set this lambda up properly with a pandas layer for future features so that I can send log statistic emails to users automatically when a new log file is loaded in it's S3 bucket.


<h2>How to Use the Project:</h2>

- Clone this project down to your local environment
- Make sure you have the Pandas package installed ```pip3 install pandas```
- Make sure you have the boto3 package installed ```pip3 install boto3```


<h3>For the first main use of this project:</h3>
  - Create a log file with the following format
    - ```<TIMESTAMP> - <APPLICATION> - <CATEGORY>[SEVERITY]: MESSAGE```
    - Ex. ```20211102T00:00 - APP - SUCCESS: No problem here.
  20211102T00:01 - APP - INFO: Some info here.
  20211102T00:02 - APP - ERROR [1]: Non-severe
  error. 20211102T00:02 - APP - ERROR [5]: Severe
  error.```
  - Call the main.py script from the terminal with the appropriate flags
    - Flags
      - -f (REQUIRED! Full path to the log file you intend to use)
      - -t (Not required. Timestamp you would like to filter the logs by)
      - -a (Not required. Application name you would like to filter the logs by. Ex. APP, SERVER, etc)
      - -c (Not required. Category that you want to filter the logs by: SUCCESS, ERROR, INFO, etc.)
      - -s (Not required. Numerical value of the severity level you want to filter the logs by: 1-5)
  - Example call ```~/main.py -f ~/logExample.out -a server -c error```
  - This will return a printout in the terminal that looks something like this
    - ```
      Error Count: 24
      Success Count: 12
      Total Count: 48

      Filtered Results:
         timestamp application category severity            message
      0   20211102T00:02         APP    ERROR        1  Non-severe error.
      1   20211102T00:02         APP    ERROR        5      Severe error.
      ```

<h3>For the second main use of this project:</h3>
  - I'm assuming for the following steps that you already have an AWS account and it is configured so that you can access your account information from your local machine's terminal.
  - Create a separate file with user subscription information with the following format.  
    - ```email - application - category```
    - Ex. ```<your_name>@example.com - APP - ERROR```
    - Note: For a single user with multiple application and/or category subscriptions means you must create a new line for each email-app-category relationship.
  - Create an S3 bucket on AWS and upload this file as an object in the bucket
    - Add the bucket name to the variable named 'user_info_bucket' on line 45 of handler.py
    - Add the object name to the variable named 'user_info_key' on line 46 of handler.py
  - Create a second S3 bucket on AWS and upload the log file you created from "The first main use of this project" and an object in this bucket
    - Add the bucket name to the variable named 'log_bucket' on line 45 of handler.py
    - Add the object name to the variable named 'log_key' on line 46 of handler.py
  - Run the handler.py script from the terminal (This script does not take any arguments)
  - Ex. ```~/handler.py```
  - This will return a printout in the terminal that looks something like this
  - ```
    To: user1@example.com
    Log Results - Application: APP Category: ERROR
         timestamp application category severity            message
    0   20211102T00:02         APP    ERROR        1  Non-severe error.
    1   20211102T00:02         APP    ERROR        5      Severe error.

    Log Results - Application: APP Category: SUCCESS
         timestamp application category severity           message
    0   20211102T00:00         APP  SUCCESS           No problem here.
    1   20211102T00:00         APP  SUCCESS           No problem here.

    Log Results - Application: SERVER Category: ERROR
    No Results


    To: user2@example.com
    Log Results - Application: APP Category: ERROR
         timestamp application category severity            message
    0   20211102T00:02         APP    ERROR        1  Non-severe error.
    1   20211102T00:02         APP    ERROR        5      Severe error.```

