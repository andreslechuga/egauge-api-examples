#!/usr/bin/env python3

# Copyright (c) 2019 eGauge Systems LLC
# 	1644 Conestoga St, Suite 2
# 	Boulder, CO 80301
# 	voice: 720-545-9767
# 	email: aaron@egauge.net
#
#                           !!! WARNING !!!
# THIS CODE HAS NOT BEEN EVALUATED FOR SECURITY AND MUST NOT BE USED
# IN A PRODUCTION OR PUBLIC ENVIRONMENT. THIS IS FOR REFERENCE AND
# EXAMPLE/TEST USE ONLY.
#
# USE CODE AT OWN RISK. EGAUGE SYSTEMS TAKES NO RESPONSIBILITY FOR DAMAGES
# INCLUDING BUT NOT LIMITED TO FINANCIAL LOSSES DUE TO USE OR MISUSE OF THIS
# CODE.


###### SETUP #######
DEVADDR  = 'DEVNAME.d.egauge.net' # enter dev URL here
USER     = None  # Add username if necessary
PASS     = None  # Add password if necessary
TIME_AGO = 24*60*60 #e.g., last 24 hours (24hr * 60m * 60s)
REG = 'use' # register name, case sensitive. use = usage, gen = generation
###### END SETUP ####

import requests # requests for HTTP requests
import xml.etree.ElementTree as ET # to parse XML
import time # to get Unix timestamps


# get Unix timestmaps for now, and now-time_ago
now  = int(time.time())
then = int(time.time())-TIME_AGO

# set up and make request
# note on parameters: 'a' = total and virtual registers
# 'T' is comma separated list of timestamps, from youngest to oldest
uri = 'http://{}/cgi-bin/egauge-show?a&T={},{}'.format(DEVADDR, now, then)
creds = requests.auth.HTTPDigestAuth(USER, PASS) # digest auth, if needed
req = requests.get(uri, timeout=10, auth=creds) # make the GET request

# req.text is the HTML response, create an ElementTree with it
root = ET.fromstring(req.text)

# for this we expect 2 'data' tags, no more no less
if len(root.findall('data')) != 2:
    print('Error, expected 2 data sets!')
    exit()

# enumerate register names with slot in XML
# "slot" is the position in the XML output, since the order of columns
# is consistent in the rows
reg_ids = {}
for child in root.findall('data'):
    for idx, cname in enumerate(child.findall('cname')):
        reg_ids[cname.text] = idx # we know REG is in slot idx in the data sets


# find the two column values in the two data sets based on the idx
now_val  = None
then_val = None
now_found = False
for child in root.findall('data'): # go into data tag
    for idx, column in enumerate(child.find('r')): # enumerate through <r> tag
        if idx == reg_ids[REG]: # we found the slot of the REG
            if not now_found: # have we already found the first 'data' tag?
                now_val = int(column.text) # no, this is the first
                now_found = True
            else:
                then_val = int(column.text) # yes, we already found the first

# energy values are in watt-seconds (joules), convert to kWh
diff = float((now_val - then_val)/3600000)
print('Difference: {} kWh'.format(diff))

# average value is kWh / hours
print('Average: {} kW'.format(diff/(TIME_AGO/60/60)))
