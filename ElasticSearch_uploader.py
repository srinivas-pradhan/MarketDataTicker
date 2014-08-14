#!/usr/bin/python

import json

def JsonToDict(jsonfile):
    try:
        json_file = open (jsonfile, "r")
        try:
            json_str = json_file.read()
            json_data = json.loads(json_str)
            return json_data
        except Exception as e:
            print e
        json_file.close()
    except IOError:
        print "Unable to read the file %s" %jsonfile
'''
This function parses the feed file exclude first line.
Returns Json object per feed line
'''
def FeedFileParser(filename):
    print "feedline"

def ESuploader(feedline, feedname, rundate ):
    print "a"