#!/usr/bin/python
import urllib2
import datetime
import time
import json
from optparse import OptionParser
import os
'''
Usage: mkdata_collector  -i config.json
This script collects the tick files from a MKDATA Source
and creates local files with naming convention KEY.YYYYMMDD
'''
# Replace all the prints with the logging function

def MkdataDaily(symbol,date, outfile):
    #URL to get data
    url="http://hopey.netfonds.no/posdump.php?date=%s&paper=%s.O&csv_format=txt" %(date, symbol)
    try:
        response = urllib2.urlopen(url)
        mkdata = response.read()
        try:
            mkdatfile = open(outfile, "w")
            
            mkdatfile.write(mkdata)
            mkdatfile.close()
            WriteToLog("Market Data for %s to file %s is written" %(symbol,outfile))
        except IOError:
            WriteToLog ("Cannot create the file %s" %outfile)
    except NameError:
        WriteToLog("The URL seems to be not functional for %s date and %s symbol"%(date,symbol))    

def WriteToLog(text):
    time = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    logdir = "/Users/srinivas/Documents/workspace/MarketDataTicker"
    logfile = "mkdata_collector.out"
    try:
        log = open (os.path.join(logdir,logfile) , "a")
        log.write(" %s | %s \n" %( time, text ))
    except Exception as e:
        WriteToLog("%s" %e )
    
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

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options] \n \nHelp: %prog -h \n\n\tOR\n\n %prog --help")
    parser.add_option("-i","--inputfile",
                      dest="inputfile",
                      default="input.json",
                      help="Input file in json format(absolute path)",
                      metavar="INPUTFILE",
                      type="str") 
    (options,args) = parser.parse_args()
    if len(args) != 1:
        parser.error("wrong number of arguments\n")

    WriteToLog("Options %s" %str(options))
    WriteToLog("Args %s" %str(args))

    #Read the json data into a Dictionary
    exchangedict = JsonToDict(options.inputfile)
    for exchangename in exchangedict:
        mksymbol = exchangedict[exchangename]
        today = time.strftime("%Y%m%d")
        mkoutfile = mksymbol + today + ".out"
        WriteToLog("Downloading the MarketData feed for %s symbol on %s run date " %(mksymbol, today))
        WriteToLog("Writing the feed to %s file" % mkoutfile)
        MkdataDaily(mksymbol,today,mkoutfile)    
    