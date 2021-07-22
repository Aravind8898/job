import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
from flask import Flask
from flask import Flask, Response
import requests
from flask import request
import csv
from flask import Flask
import pymongo
from flask import request
from pymongo import MongoClient
import json
from bson import json_util

def get_url(position, location):
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

position1 = input("Please enter the job profile you want to search for : ")
location1 = input("Please enter the location for you want to search this job profile: ")

url = get_url(position1, location1)

response = requests.get(url)
#print(response)
#print(response.reason)

soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('div', 'job_seen_beacon')
#print(len(cards))

card = cards[0]
atag = card.h2.span
job_title = atag.get('title')
#print(job_title)
job_company_name = card.find('span',{'class':'companyName'}).text
#print(job_company_name)
job_location = card.find('div', {'class':'companyLocation'}).text
#print(job_location)
try:
    job_salary = card.find('span', {'class': 'salary-snippet'}).text.strip()
except AttributeError:
    job_salary = "Salary Not Mentioned"
#print(job_salary)
job_details = card.find('div', {'class':'job-snippet'}).text.strip()
#print(job_details)
job_date = card.find('span', {'class':'date'}).text
#print(job_date)
today_date = datetime.today().strftime('%d-%m-%y').strip()
#print(today_date)
#print(line_gap)

def get_record(card):
    atag = card.h2.span
    job_title = atag.get('title')
    #print(job_title)
    job_company_name = card.find('span', {'class': 'companyName'}).text
    #print(job_company_name)
    job_location = card.find('div', {'class': 'companyLocation'}).text
    #print(job_location)
    try:
        job_salary = card.find('span', {'class': 'salary-snippet'}).text.strip()
    except AttributeError:
        job_salary = "Salary Not Mentioned"
    #print(job_salary)
    job_details = card.find('div', {'class': 'job-snippet'}).text.strip()
    #print(job_details)
    job_date = card.find('span', {'class': 'date'}).text
    #print(job_date)
    today_date = datetime.today().strftime('%d-%m-%y').strip()
    #print(today_date)

    #print(line_gap)

    record = (job_title, job_company_name, job_location, job_salary, job_details, job_date, today_date)
    return record

records = []
for card in cards:
    record = get_record(card)
    records.append(record)

#print(records)

while True:
    try:
        url = 'https://in.indeed.com/' + soup.find('a', {'aria-label': 'Next'}).get('href')
    except AttributeError:
        break

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', 'job_seen_beacon')

    for card in cards:
        record = get_record(card)
        records.append(record)

    #print(records[21])

    print(len(records))


   ############################################## PUTTING ALL TOGETHOR ##############################

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(position, location):
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def get_record(card):
    atag = card.h2.span
    job_title = atag.get('title')
    #print(job_title)
    job_company_name = card.find('span', {'class': 'companyName'}).text
    #print(job_company_name)
    job_location = card.find('div', {'class': 'companyLocation'}).text
    #print(job_location)
    try:
        job_salary = card.find('span', {'class': 'salary-snippet'}).text.strip()
    except AttributeError:
        job_salary = "Salary Not Mentioned"
    #print(job_salary)
    job_details = card.find('div', {'class': 'job-snippet'}).text.strip()
    #print(job_details)
    job_date = card.find('span', {'class': 'date'}).text
    #print(job_date)
    today_date = datetime.today().strftime('%d-%m-%y').strip()
    #print(today_date)
    #print(line_gap)

    record = (job_title, job_company_name, job_location, job_salary, job_details, job_date, today_date)
    return record

def main(position, location):
    records = []
    url = get_url(position, location)

#EXTRACTING THE JOB DATA
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'job_seen_beacon')

        for card in cards:
            record = get_record(card)
            records.append(record)

        try:
            url = 'https://in.indeed.com/' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break

#SAVING THE JOB DATA
        with open('results2.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['job_title', 'job_company_name', 'job_location', 'job_salary', 'job_details', 'job_date', 'today_date'])
            writer.writerows(records)

main(position1, location1)
