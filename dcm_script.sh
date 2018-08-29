#!/bin/bash
# NOTE: copy and paste this command into the terminal instead of running this script
# Running the script will end the process on exit 
nohup python /root/dcm/dcm.py >> /root/dcm/logs.out 2>&1 &
