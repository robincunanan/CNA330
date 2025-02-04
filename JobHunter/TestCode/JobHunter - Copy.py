# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# Fall 2019 CNA 330
# Robin Cunanan, rtcunanan@student.rtc.edu
import mysql.connector
import sys
import json
import urllib.request
import os
import time

# Connect to database
# You may need to edit the connect function based on your local settings.
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cna330')
    return conn

# Create the table structure
def create_tables(cursor, table):
    ## Add your code here. Starter code below
    cursor.execute('''CREATE TABLE IF NOT EXISTS tablename (id INT PRIMARY KEY auto_increment, Type varchar(10), Title varchar(100), Description text,
    Job_id varchar(33), Created_at DATE, Company varchar(100), Location varchar(50), How_to_apply varchar(100)); ''')
    return

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor

# Add a new job
def add_new_job(cursor, jobdetails):
    ## Add your code here
    query = "INSERT INTO"
    return query_sql(cursor, query)

# Check if new job
def check_if_job_exists(cursor, jobdetails):
    ## Add your code here
    query = "SELECT"
    return query_sql(cursor, query)

def delete_job(cursor, jobdetails):
    ## Add your code here
    query = "UPDATE"
    return query_sql(cursor, query)

# Grab new jobs from a website
def fetch_new_jobs(arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?location=seattle" #"https://jobs.github.com/positions.json?" + "location=seattle" ## Add arguments here #Use & after seattle to do &description=python&full_time=no this is how to chain
    jsonpage = 0
    try:
        contents = urllib.request.urlopen(query)
        response = contents.read() #Loads from configuartion file
        jsonpage = json.loads(response) # checks database, any jobs that find
    except:
        pass
    return jsonpage

# Load a text-based configuration file
def load_config_file(filename):
    argument_dictionary = 0
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path = os.path.abspath(os.path.dirname(__file__))
    file = 0
    file_contents = 0
    try:
        file = open(filename, "r")
        file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()

    ## Add in information for argument dictionary
    return argument_dictionary

# Main area of the code.
def jobhunt(arg_dict): # Important, rest are supporting functions 
    # Fetch jobs from website
    jobpage = fetch_new_jobs(arg_dict) #gets github website and holds the json data in it
    # print(jobpage)
    ## Add your code here to parse the job page # hint import json, use it's module converts json to a python dictionary
    jobpage_parsed = json.load(jobpage)

    ## Add in your code here to check if the job already exists in the DB #print like new job is found

    ## Add in your code here to notify the user of a new posting

    ## EXTRA CREDIT: Add your code to delete old entries #if over a month old delete them

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main(): # Important, rest are supporting functions 
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "table")
    # Load text file and store arguments into dictionary
    arg_dict = 0
    while(1): # Infinite Loops. Only way to kill it is to crash or manually crash it. We did this as a background process/passive scraper
        jobhunt(arg_dict) # arg_dict is argument dictionary, 
        time.sleep(3600) # Sleep for 1h, this is ran every hour because API or web interfaces have request limits. Your reqest will get blocked.
# Sleep does a rough cycle count, system is not entirely accurate
if __name__ == '__main__':
    main()
