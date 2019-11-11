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
    cursor.execute('''CREATE TABLE IF NOT EXISTS Jobs (id INT PRIMARY KEY AUTO_INCREMENT, PostDate TEXT, Title TEXT, Location TEXT, Description TEXT, Company TEXT, Apply_info TEXT, Salary FLOAT, RawMessage TEXT, Github_ID TEXT); ''')
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
def fetch_new_jobs(cursor, arg_dict):
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/Sql.py
    query = "https://jobs.github.com/positions.json?description=&location=washington" # Add arguments here
    jsonpage = 0
    contents = urllib.request.urlopen(query)
    response = contents.read()
    jsonpage = json.loads(response)
    for page in jsonpage:
        print(page['location'])
        page['description'] = str(page['description']).replace('\"', '')
        page['how_to_apply'] = str(page['description']).replace('\"', '')
        cursor.execute('''INSERT INTO Jobs (PostDate, Title, Location, Description, Company, Apply_info) VALUES (
        "''' + page['created_at'] + '''",
        "''' + page['title'] + '''",
        "''' + page['location'] + '''",
        "''' + page['description'] + '''",
        "''' + page['company'] + '''",
        "''' + page['how_to_apply'] + '''")''')


# Load a text-based configuration file
def load_config_file(filename):
    argument_dictionary = []
    # Code from https://github.com/RTCedu/CNA336/blob/master/Spring2018/FileIO.py
    rel_path = os.path.abspath(os.path.dirname(__file__))
    file = 0
    file_contents = 0
    try:
        file = open(filename, "r")
        #file_contents = file.read()
    except FileNotFoundError:
        print("File not found, it will be created.")
        file = open(filename, "w")
        file.write("")
        file.close()

    ## Add in information for argument dictionary

    for aline in file:
        aline = aline.strip()
        argument_dictionary.append(aline)

    file.close()
    return argument_dictionary

# Main area of the code.
def jobhunt(cursor, arg_dict):
    # Fetch jobs from website
    jobpage = fetch_new_jobs(cursor, arg_dict)
    # print (jobpage)
    ## Add your code here to parse the job page
    #from bs4 import BeautifulSoup
    #import requests

    #job_soup = "https://seattle.craigslist.org/search/jjj"
    #r = requests.get(job_soup)
    #soup = BeautifulSoup(r.text, 'html.parser')
    ### print(r.text)
    ### grid-list-container
    #soup_name = soup.find_all('p')
    ### print(soup_name)
    #soup_names = []
    #for i in range(3, 12):
    #soup_names.append(soup.find_all('p')[i].get_text())
    #for i in range(0, len(soup_names)):
    #soup_names[i] = soup_names[i].replace('\t', '')
    #soup_names[i] = soup_names[i].replace('\n', '')
    #print(soup_names)

    ## Add in your code here to check if the job already exists in the DB

    ## Add in your code here to notify the user of a new posting

    ## EXTRA CREDIT: Add your code to delete old entries

# Setup portion of the program. Take arguments and set up the script
# You should not need to edit anything here.
def main():
    # Connect to SQL and get cursor
    conn = connect_to_sql()
    cursor = conn.cursor()
    create_tables(cursor, "table")
    # Load text file and store arguments into dictionary
    arg_dict = load_config_file(sys.argv[1])
    while(1):
        jobhunt(cursor, arg_dict)
        conn.commit()
        time.sleep(3600) # Sleep for 1h


if __name__ == '__main__':
    main()