#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set of functions to query the Oireachtas api at
https://api.oireachtas.ie/v1/
"""
import os
from json import *
from datetime import *
import requests
import json


#LEGISLATION_DATASET = 'legislation.json'
#MEMBERS_DATASET = 'members.json'

#Request and save json data

LEGISLATION_REQUEST = 'https://api.oireachtas.ie/v1/legislation?bill_status=Current,Withdrawn,Enacted,Rejected,Defeated,Lapsed&bill_source=Government,Private%20Member&date_start=1900-01-01&date_end=2099-01-01&limit=50&chamber_id=&lang=en'
MEMBERS_REQUEST= 'https://api.oireachtas.ie/v1/members?date_start=1900-01-01&chamber_id=&date_end=2099-01-01&limit=50'
LEGISLATION_DATASET = "leg.json"
MEMBERS_DATASET = "mem.json"


#Get JSON data, and save it to offline files.
legGet = requests.get(LEGISLATION_REQUEST)
memGet = requests.get(MEMBERS_REQUEST)
legGet = legGet.json()
memGet = memGet.json()

with open("leg.json", 'w') as f:
    json.dump(legGet, f)

with open("mem.json", 'w') as f:
    json.dump(memGet, f)
#Data is now saved.

#Allow the keyword "load" to be used to open files
load = lambda jfname: loads(open(jfname).read())


def filter_bills_sponsored_by(pId):
    """Return bills sponsored by the member with the specified pId

    :param str pId: The pId value for the member
    :return: dict of bill records
    :rtype: dict
    """
    leg = load(LEGISLATION_DATASET)
    mem = load(MEMBERS_DATASET)

    ret = []

    for res in leg['results']:
        p = res['bill']['sponsors']
        for i in p:
            name = i['sponsor']['by']['showAs']
            for result in mem['results']:
                fname = result['member']['fullName']
                rpId = result['member']['pId']
                if fname == name and rpId == pId:
                    print("\n", name, "!")
                    ret.append(res['bill'])


    

    #Alternative method using list comprehensions

    # #Create list of members
    # results = mem["results"]
    # members = [entry["member"] for entry in results]

    # #Create dictionary of IDs to names
    # dictionary = {i["pId"]:i["fullName"] for i in members}
   
    # #Now: Using the name associated to this pId, find the bills this member has done.
    # member_name = dictionary[pId]

    # bills = []

    # for entry in leg["results"]:
    #     #p.append(entry["bill"]["sponsors"])
    #     g = entry["bill"]["sponsors"]

    #     for i in g:
    #         name = i["sponsor"]["by"]["showAs"]
    #         if(name == member_name):
    #             bills.append(entry["bill"])
    

    
    return ret


def filter_bills_by_last_updated(since, until):
    """Return bills updated within the specified date range

    :param datetime.date since: The lastUpdated value for the bill
        should be greater than or equal to this date
    :param datetime.date until: The lastUpdated value for the bill
        should be less than or equal to this date. If unspecified, until
        will default to today's date
    :return: List of bill records
    :rtype: list

    """

    #Number of characters to be removed (from right to left) from lastUpdated string
    HOURSMINSSEC = 22

    #If not given an 'Until' time, make one
    if until == None: until = datetime.today()

    #Use list comprehension to parse through the leg data, filtering out those entries with updates outside of the specified range
    #Return the resultant list.

    try:
    
        leg = load(LEGISLATION_DATASET)
        
        results = leg['results']

        dates = []
        bills = []

        #Parse the lastUpdated value for each bill.
        dates = [entry['bill']['lastUpdated'] for entry in results]
        bills = [entry['bill'] for entry in results]

        #For each date, check if they lie within the range of since and until
        #First cut off any unnecessary parts of the strings. Then remove any entries outside of range
        
        for index, date in enumerate(dates):
            date = date[:-HOURSMINSSEC]
            date = datetime.strptime(date, "%Y-%m-%d")
            dates[index] = date
            if(dates[index] > until or dates[index] < since):
                #print("\n")
                #print(dates[index])
                #print(bills[index]["billNo"])
                dates.pop(index)
                bills.pop(index)

        #print("\n" + str(len(dates)) + " " + str(len(bills)))

        return bills

    except: 
        raise NotImplementedError
