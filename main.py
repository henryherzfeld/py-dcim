# Append parent directory to sys.path list

from __future__ import print_function
import copy
import netsnmp
from time import time
from time import sleep
import sys
from datetime import datetime 
import dcim

# IMPORT INITIAL CONFIG
execfile('/root/dcm/conf.py')


# Main Loop
def main():
    act_int = dcim.interval
    dcim.eprint (dcim.getDateTime(), "\nStarting Data Center Monitoring...\n")
    print ("Interval Time :", act_int, " sec /", round((act_int/60.0),2) ," min")
    EarliestDate = getEarliestDate()
    print ("Oldest Date       :", EarliestDate)
    while True:
	execfile('/root/dcm/conf.py')
        gatherLoop(EarliestDate)

main()
