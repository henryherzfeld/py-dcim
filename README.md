DCIM_fau 
==========

![](https://img.shields.io/badge/build-alpha-blue.svg)

### Features

- Autonomous data collection via SNMP 
- Supports Python 2.7 and up
- Lightweight, no dependencies (non-standard, 2.7+)
- Available on PyPi

About
-------------

DCIM_fau is a Python program designed to simplify deploying and monitoring large SNMP-based networking interfaces.



Getting Started 
----
DCIM_fau is quick to deploy and even quicker to run.

#### 1. Installation
Firstly, pull the package from either PyPi or Github:

 &nbsp; &nbsp; &nbsp; &nbsp; `$ pip install dcim_fau` &nbsp; &nbsp; &nbsp; &nbsp; _installation via pip package manager is **always** preferred_

#### 2. _conf.yaml_
The configuration file for DCIM_fau uses markdown to notate specific parameters required to run in a readable format.
 
 ##### &nbsp; &nbsp; _conf.yaml_ example
```YAML    
# SNMP "secret"
  snmp:
    - COMM_STRING: 'mySNMPsecre'

  chron:
# collection interval (seconds)
   - COLLECT_INTERVAL: 120

# deletion interval (months)
   - DELETE_INTERVAL: 4

# MYSQL connection info
  db:
    - DB_HOST: 'localhost'
    - DB_USER: 'root'
    - DB_PASSWORD: 'admin'
    - DB_NAME: 'deebee'
```
        
 &nbsp; &nbsp; You **must** include your _conf.yaml_ in your DCIM_fau root directory, with all parameters validated.

#### 3. Initialize and Run
##### Initialization:

DCIM_fau utilizes Python's `console_scripts` entry point logic to simplify deployment and execution.

To initialize, run the following command:

`$ dcim_fau:scaffold`

This scaffolds the database, building the necessary structure for the provided equipment OIDs.

##### Run:
To start collection, run the following command:

`$ dcim_fau:run`

Roadmap*
-------

| Release   | Target Date |
| :--------- | -----:|
| Alpha     | Sept. 20th |
| Beta      | Oct. 15th    | 
| 1.0       | November 10th |

<sup>*The dates for all release windows are tentative</sup>

The MIT License (MIT)
=====================

Copyright © 2018 Henry Herzfeld

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the “Software”), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
