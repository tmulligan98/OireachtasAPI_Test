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

LEGISLATION_DATASET = 'https://api.oireachtas.ie/v1/legislation?bill_status=Current,Withdrawn,Enacted,Rejected,Defeated,Lapsed&bill_source=Government,Private%20Member&date_start=1900-01-01&date_end=2099-01-01&limit=50&chamber_id=&lang=en'
MEMBERS_DATASET = 'https://api.oireachtas.ie/v1/members?date_start=1900-01-01&chamber_id=&date_end=2099-01-01&limit=50'

load = lambda jfname: loads(open(jfname).read())

def filter_bills_sponsored_by(pId):
    """Return bills sponsored by the member with the specified pId

    :param str pId: The pId value for the member
    :return: dict of bill records
    :rtype: dict
    """
    #leg = load(LEGISLATION_DATASET)
    #mem = load(MEMBERS_DATASET)

    leg = requests.get(LEGISLATION_DATASET)
    mem = requests.get(MEMBERS_DATASET)

    #print(leg.status_code)
    #print(mem.status_code)

    #text = json.dumps(leg.json(), sort_keys = True, indent=4)
    #print(text)



    ret = []

    for res in leg['results']:
        p = res['bill']['sponsors']
        for i in p:
            name = i['sponsor']['by']['showAs']
            for result in mem['results']:
                fname = result['member']['fullName']
                rpId = result['member']['pId']
                if fname == name and rpId == pId:
                    ret.append(res['bill'])


    

    # #Create list of members
    # members = [mems for mems in mem['results']['member']]
    # #Using dict comprehension, now have dictionary of pIds and their respective full names
    # dictionary = {i["pId"]:i["fullName"] for i in members}

    
    # #Now: Using the name associated to this pId, find the bills this member has done.
    # member_name = dictionary[pId]

    # #With this member name, add all bills with this member name to the ret variable
    # results = leg["results"]
    # ret = [bill for bill in leg['results'] if member_name in bill]
   

    
    





    
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
    raise NotImplementedError
