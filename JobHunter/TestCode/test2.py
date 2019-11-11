# This script pulls from a job website and stores positions into a database. If there is a new posting it notifies the user.
# CNA 330
# Zachary Rubin, zrubin@rtc.edu
import mysql.connector
import sys
import json
import urllib.request
import os
import time

# Connect to database
# You should not need to edit anything in this function
def connect_to_sql():
    conn = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  database='cna330')
    return conn

# Create the table structure
def create_tables(cursor, table):
    ## Add your code here. Starter code below
    cursor.execute('''CREATE TABLE IF NOT EXISTS JOBS (id INT PRIMARY KEY auto_increment, PostDate Date, Title TEXT, Location TEXT, Description TEXT, Company TEXT, Apply_info TEXT, Salary FLOAT, RawMessage TEXT );''')
    return

# Query the database.
# You should not need to edit anything in this function
def query_sql(cursor, query):
    cursor.execute(query)
    return cursor

# Add a new job
def add_new_job(cursor, job):
    ## Add your code here
    job = job[0]
    data = (job['created_at'], job['title'],job['location'],job['description'], job['company'], job['how_to_apply'], 'money',str(job))
    query = 'INSERT INTO JOBS (id, PostDate, Title, Location, Description, Company, Apply_info, Salary, RawMessage)'
    'values ("%s", "%s", "%s", "%s", "%s", "%s", "%s","%s") '
    cursor.execute(query,data)

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
    sea = "seattle"
    description = "description"
    salary = "salary"
    location = "location"
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json"#?" + "location= " + sea + " & decription =" + location + salary #Add arguments here
    jsonpage = 0

    try:
        contents = urllib.request.urlopen(query)
        response = contents.read()
        jsonpage = json.loads(response)


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
def jobhunt(arg_dict):
    # Fetch jobs from website
    return fetch_new_jobs(arg_dict)
    # print (jobpage)
    ## Add your code here to parse the job page

    ## Add in your code here to check if the job already exists in the DB

    ## Add in your code here to notify the user of a new posting

    ## EXTRA CREDIT: Add your code to delete old entries

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "JOBS")
    # Load text file and store arguments into dictionary
    arg_dict = 0
    while(1):
        add_new_job(cursor,jobhunt(arg_dict))
        time.sleep(3600) # Sleep for 1h

if __name__ == '__main__':
    main()
