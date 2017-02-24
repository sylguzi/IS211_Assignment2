#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 2"""
import datetime
import csv
import urllib2
import logging
import argparse

def downloadData(url):
    """
    Read a URL and return its content as string

    :param some_url:
    :return:
    """
    return urllib2.urlopen(url).read()

def processData(content, assignment2):
    """
    Takes a string as CSV and do some magic

    :param response_html:
    :return:
    """
    personData = {}
    # split the content by '\n' to get each line individually
    # each line from the csv file will be convert to a person dictionary and put into a list
    parsedData = csv.DictReader(content.split('\n'))
    count = 0

    # we enumerate the list therefore the index will be the line_number - 1
    for index, person in enumerate(parsedData):
    # we use the person id multiple time so we put it into a variable
        id = person['id']
        try:
            # parsing person data and insert it into personData
            personData[id] = (person['name'],
                datetime.datetime.strptime(person['birthday'], '%d/%m/%Y'))
            count += 1
        except:
            assignment2.error('Error processing line #{} for ID #{}'
                                .format(index + 1, id))

    return personData, count

def displayPerson(id, personData):
    """Displays the information unless no ID is found
    """
    try:
        (name, birthday) = personData[str(id)]
        print('Person #{} is {} with a birthday of {}'.format(
        id,
        name,
        birthday.strftime('%Y-%m-%d')))
    except:
        print('No result found with that id {}'.format(id))

def parseParam():
    """Parses the data
    """
    parser = argparse.ArgumentParser(description=
	'Parsing a file and give person information based on user input')
    parser.add_argument('-u','--url',
        help='The url where the program will need to download person data',
	required=True)
    return parser.parse_args()

def createLogger(filename='errors.log'):
    """Creates logger; writes to the handler
    """
    logger = logging.getLogger('assignment2')
    hdlr = logging.FileHandler(filename, mode='w')
    logger.addHandler(hdlr)
    return logger

def readRawInput(personData):
    """Takes in user input. Exits if input is <=0, but otherwise gives info
    """
    while(True):
        try:
            id = int(raw_input("Enter the id of the person you want to see the information: "))
            if(id <= 0):
                exit(0)
            else:
                displayPerson(id, personData)
        except Exception as err:
            print(err)

if __name__ == '__main__':
    parameter = parseParam()
    URL = parameter.url
    try:
        csvData = downloadData(URL)
        assignment2 = createLogger()
        (personData, count) = processData(csvData, assignment2)
        #print('There is {} person in the dictionary', count)
        readRawInput(personData)
    except Exception as err:
        sprint(err)
