DCIM_fau 
==========

![](https://img.shields.io/badge/build-alpha-blue.svg)

### Features

- Asynchronous data collection via PySNMP 
- Redis 5.0 streams
- Available on PyPi

About
-------------

DCIM_fau is a Python program designed to simplify deploying and monitoring large SNMP-based networking interfaces.



Getting Started 
----
DCIM_fau is quick to deploy and even quicker to run.

#### 1. Installation
Firstly, pull the package from either PyPi or Github:

 &nbsp; &nbsp; &nbsp; &nbsp; `$ pip install dcim-fau` &nbsp; &nbsp; &nbsp; &nbsp; _installation via pip package manager is preferred_

#### 2. _conf.yaml_
The configuration file for DCIM_fau uses markdown to notate specific parameters required to run in a readable format.
 
 ##### &nbsp; &nbsp; _conf.yaml_ example
```YAML    
snmp:
  COMM_STRING: 'myCommunityString'
  TIMEOUT: 20

stream:
  STREAM_HOST: '127.0.0.1'
  STREAM_ID: 'localstream'
  STREAM_PASS: 'password'
  STREAM_PACKET: '100'

chron:
  COLL_INTERVAL: 180

targets:
  1:
    rack:
    row: A
    equipment:
    - type: my_equipment
      ip: 10.0.0.1
...
...

oids:
  my_equipment:
  - my_data_1:
      value: '1.3.6.1...'
      divisor: 10
  - my_data_2:
      value: '1.3.6.1...'
      divisor: 10
  - my_data_3:
      value: '1.3.6.1...'
      divisor: 10
...
```
        
 &nbsp; &nbsp; You **must** include your _conf.yaml_ in your DCIM_fau root directory, with all parameters validated.

#### 3. Initialize and Run
##### Initialization:

DCIM_fau utilizes Python's `console_scripts` entry point logic to simplify deployment and execution.

##### Run:
To start collection, run the following command:

`$ run &`

##### Test:
To run a set of initialization tests:

`$ test`


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
