from __future__ import print_function
import copy
import netsnmp
from time import time
from time import sleep
import sys
from datetime import datetime 

# IMPORT INITIAL CONFIG
execfile('/root/dcm/conf.py')

# Prints messages to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Calls snmpGet and returns values
def snmpGet(ip, oid, div):
    session = netsnmp.Session(DestHost=ip, Version=2, Community=comm)
    vars = netsnmp.VarList(netsnmp.Varbind(oid))
    v = session.get(vars)
    if(str(v[0]) == '-1'):
        eprint (getDateTime(), "OID not used on device", oid, "from IP", ip, sep=": ")
        sys.exit("OID not used on device")
    elif(v[0] == ''):
        eprint (getDateTime(), "Error in OID", oid, "from IP", ip, sep=": ")
        return ''
    else:
	try:
            ret = round((float(v[0])/div),1)
            return str(ret)
	except:
            if(v[0] == None):
                return
            else:
                eprint (getDateTime(), "Unknown Error ", v[0], sep=": ")

# Called by the classes, will return an dictionary of
# a walkthrough of each oid and its date-time stamp
def oidWalk(oid_arr, ip, sensor):
    vals = []
    for v in oid_arr:
        o = ''.join([v[1], sensor])
        #print v
        val = snmpGet(ip, o, v[2])
        if(val != None):
            vals.append([v[0], snmpGet(ip, o, v[2])])
    return (vals)

# Return date and time in proper format
def getDateTime():
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dt

# Insert values into database
def insertData(device_dt, rack_id, device_id, device_arr):
    # Insert values into DB from row and rack id
    sql = "INSERT INTO " + device_id +  "(" + "rack_id, " + "reading_dt"
    val = " VALUES (" + "'" + rack_id + "', '" + device_dt + "'"
    for x in range(0, len(device_arr)):
        try:
            sql = sql + ", " + device_arr[x][0]
            val = val + ", '" + device_arr[x][1] + "'"
        except:
            eprint (getDateTime(), "Error in either device_arr[x][0]", device_arr[x][0], " or device_arr[x][1]", device_arr[x][1], sep=": ")
    sql = sql + ") "
    val = val + ");"
    sql = sql + val
    try:
        c.execute(sql)
        conn.commit()
    except:
        eprint (getDateTime(), "Error in SQL Insert", sql, sep=": ")

# Get array thats stored all information for storage
# arr[row_id, rack_number, reading_name, reading_value, date-time]
def storeData(row_dic, date_dt):
    for row_id, rack_dic in row_dic.items():
        for rack_number, device_arr_dic in rack_dic[1].items():
            values = []
            for device_id, device_arr_arr in device_arr_dic.items():
                # Get database row_id
                sql=''.join(["SELECT rack_id FROM rack WHERE row_id='", row_id, "' AND rack_number='", rack_number, "'"])
                try:
                    c.execute(sql)
                    conn.commit()
                except:
                    eprint (getDateTime(), "Error in SQL select", sql, sep=": ")
                rid = c.fetchall()
                rack_id = str(rid[0][0])
                # Should only return one row
                if(len(rid) != 1):
                    eprint (getDateTime(), "Multiple rows on rack_id query", sql, sep=": ")
                    break
                else:
                    for device_arr in device_arr_arr:
                        for v in device_arr:
                            # Combine each device in a rack into one array
                            values.append(v)

                # Insert combined rack into database
                insertData(date_dt, rack_id, device_id, values)                   


# Returns the earliest date from 'reading' table
def getEarliestDate():
    sql = "SELECT min(mx) FROM (SELECT max(reading_dt) AS `mx` FROM ups1 UNION SELECT max(reading_dt) AS `mx` FROM ups2 UNION SELECT max(reading_dt) AS `mx` FROM rpdu UNION SELECT max(reading_dt) AS `mx` FROM inlinerp) AS t1;"
    try:
        c.execute(sql)
        conn.commit()
        ed = c.fetchall()
	if(ed[0][0]==None):
            print ("No Earliest Record")
	    dt = getDateTime()
	    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        else:
            return ed[0][0]
    except:
        eprint (getDateTime(), "Error in SQL select (getting oldest date)", sql, sep=": ")

# Deletes all data that is over 2 years old
def deleteOldData(EarliestDate):
    tables = ["rpdu", "ups1", "ups2", "inlinerp"]
    mi = EarliestDate.month + monthinterval
    if(mi > 12):
        dtcmp = EarliestDate.replace(month=(mi%12), year=(EarliestDate.year-1))
    else:
        dtcmp = EarliestDate.replace(month=(mi))

    if(datetime.now() <= dtcmp):
        return

    for v in tables:
        sql = ''.join(["DELETE FROM ",v," WHERE reading_dt < DATE_SUB(CURDATE(), INTERVAL ", str(monthinterval), " MONTH);"])
        try:
            print (sql)
            c.execute(sql)
            conn.commit()
        except:
            eprint (getDateTime(), "Error in SQL (deleting old data)", sql, sep=": ")


# Class with regards to all UPS devices
class Ups1:
    ip = ''
    def __init__(self, ip):
        self.ip = ip
    # Go through each OID and return the respective value
    def Get(self):
        return oidWalk(upsOids, self.ip,  '')

# Power Distribution Unit
class Ups2:
    ip = ''
    def __init__(self, ip):
        self.ip = ip
    def Get(self):
        return oidWalk(ups2Oids, self.ip,  '')
    
class RackPdu_a:
    ip = ''
    oids = []
    for x in range(0, len(rackPduOids)):
        oids.append(["pdua_" + rackPduOids[x][0], rackPduOids[x][1], rackPduOids[x][2]])
    def __init__(self, ip):
       self.ip = ip
    def Get(self):
        return oidWalk(self.oids, self.ip,  '')

class RackPdu_b:
    ip = ''
    oids = []
    for x in range(0, len(rackPduOids)):
        oids.append(["pdub_" + rackPduOids[x][0], rackPduOids[x][1], rackPduOids[x][2]])
    def __init__(self, ip):
       self.ip = ip
    def Get(self):
        return oidWalk(self.oids, self.ip,  '')

# OID is defined by initilaization
class ACRackTemp:
    # [name, oid, divisor]            
    oids = []
    ip = ''
    def __init__(self, ip, rid):
        self.ip = ip
        rid = int(rid)
	if(rid > int(3) or rid < int(1)):
	    sys.exit("rid not equal to 1, 2, or 3")
	tmp = 'airIRRP100UnitStatusRackInletTemperature' + str(rid) + 'Metric.0'
	tmp2 = "temp2"
	self.oids = [(tmp2, tmp, 10)]
    def Get(self):
        return oidWalk(self.oids, self.ip,  '')
       
class AC:
    ip = ''
    def __init__(self, ip):
        self.ip = ip
    def Get(self):
        return oidWalk(acOids, self.ip,  '')

class TempSensor:
    ip = ''
    sensor = ''
    def __init__(self, sensor, ip):
        self.sensor = sensor
        self.ip = ip
    def Get(self):
        return oidWalk(tempSensorOids, self.ip,  self.sensor)

class HumiSensor:
    ip = ''
    sensor = ''
    def __init__(self, sensor, ip):
        self.sensor = sensor
        self.ip = ip
    def Get(self):
        return oidWalk(humiSensorOids, self.ip,  self.sensor)

# Currently Not in Use
# Can be added to array list if needed
class DewPointSensor:
    # [name, oid, divisor]            
    ip = ''
    sensor = ''
    def __init__(self, sensor, ip):
        self.sensor = sensor
        self.ip = ip
        def Get(self):
            return oidWalk(dewPointOids, self.ip,  self.sensor)

# ARRAY OF ALL OIDS FOR A GIVEN RACK
# [dbname, [device classes]]
a2 = ["ups1", [
    Ups1('10.15.30.184')
]]
a3 =["ups2", [
    Ups2('10.15.30.186')
]]
a4 =["rpdu", [
    RackPdu_a('10.15.30.151'),
    RackPdu_b('10.15.31.154'),
    TempSensor('3406802758', '10.15.30.193'),
    ACRackTemp("10.15.31.155", 3),
    HumiSensor('3273299739', '10.15.30.193')
]]
a5 =["rpdu", [
    RackPdu_a('10.15.30.189'),
    RackPdu_b('10.15.31.154'),
    ACRackTemp("10.15.31.155", 2),
    TempSensor('1619732064', '10.15.30.193'),
    HumiSensor('1974269701', '10.15.30.193')
]]
a6 =["inlinerp", [
    AC('10.15.31.155')
]]
a7 =["rpdu", [
    RackPdu_a('10.15.30.156'),
    RackPdu_b('10.15.30.157'),
    ACRackTemp("10.15.31.155", 1),
    TempSensor('2628357572', '10.15.30.193'),
    HumiSensor('2804425567', '10.15.30.193')
]]
a8 =["rpdu", [
    RackPdu_a('10.15.30.158'),
    RackPdu_b('10.15.30.159'),
    TempSensor('1665932156', '10.15.30.193'),
    HumiSensor('1668196833', '10.15.30.193')
]]
a9 =["rpdu", [
    RackPdu_a('10.15.30.160'),
    RackPdu_b('10.15.30.161'),
    ACRackTemp("10.15.30.162", 3),
    TempSensor('3328914949', '10.15.30.193'),
    HumiSensor('581338442', '10.15.30.193')
]]
a10 =["inlinerp", [

    AC('10.15.30.162')
]]
a11 =["rpdu", [
    RackPdu_a('10.15.30.163'),
    RackPdu_b('10.15.30.164'),
    ACRackTemp('10.15.30.162', 2),
    TempSensor('242089423', '10.15.30.193'),
    HumiSensor('338404919', '10.15.30.193')
]]
a12 =["rpdu", [
    RackPdu_a('10.15.30.165'),
    RackPdu_b('10.15.30.166'),
    ACRackTemp('10.15.30.162', 1),
    TempSensor('2716713264', '10.15.30.193'),
    HumiSensor('976244450', '10.15.30.193')
]]

b2 =["ups1", [
    Ups1('10.15.30.185')
]]
b3 =["ups2", [
    Ups2('10.15.30.183')
]]
b4 =["rpdu", [
    RackPdu_a('10.15.30.167'),
    RackPdu_b('10.15.30.168'),
    ACRackTemp('10.15.30.171', 3),
    TempSensor('3406802758', '10.15.30.191'),
    HumiSensor('3273299739', '10.15.30.191')
]]
b5 =["rpdu", [
    RackPdu_a('10.15.30.169'),
    RackPdu_b('10.15.30.200'),
    ACRackTemp('10.15.30.171', 2),
    TempSensor('1619732064', '10.15.30.191'),
    HumiSensor('1974269701', '10.15.30.191')
]]
b6 =["inlinerp", [
    AC('10.15.30.171')
]]
b7 =["rpdu", [
    RackPdu_a('10.15.30.172'),
    RackPdu_b('10.15.30.173'),
    TempSensor('2628357572', '10.15.30.191'),
    HumiSensor('2804425567', '10.15.30.191')
]]
b8 =["rpdu", [
    RackPdu_a('10.15.30.174'),
    RackPdu_b('10.15.30.175'),
    ACRackTemp('10.15.30.171', 1),
    TempSensor('1665932156', '10.15.30.191'),
    HumiSensor('1668196833', '10.15.30.191')
]]
b9 =["rpdu", [
    RackPdu_a('10.15.30.176'),
    RackPdu_b('10.15.30.177'),
    ACRackTemp('10.15.30.178', 3),
    TempSensor('3328914949', '10.15.30.191'),
    HumiSensor('581338442', '10.15.30.191')
]]
b10 =["inlinerp", [
    AC('10.15.30.178')
]]
b11 =["rpdu", [
    RackPdu_a('10.15.30.179'),
    RackPdu_b('10.15.30.180'),
    ACRackTemp('10.15.30.178', 2),
    TempSensor('242089423', '10.15.30.191'),
    HumiSensor('338404919', '10.15.30.191')
]]
b12 =["rpdu", [
    RackPdu_a('10.15.30.181'),
    RackPdu_b('10.15.30.182'),
    ACRackTemp('10.15.30.178', 1),
    TempSensor('2716713264', '10.15.30.191'),
    HumiSensor('976244450', '10.15.30.191')
]]

# DICTIONARY OF EACH RACK NUMBER FOR A GIVEN RACK ARRAY 
A_Row = {
    "2" : a2,
    "3" : a3,
    "4" : a4,
    "5" : a5,
    "6" : a6,
    "7" : a7,
    "8" : a8,
    "9" : a9,
    "10" : a10,
    "11" : a11,
    "12" : a12
}

B_Row = {
    "2" : b2,
    "3" : b3,
    "4" : b4,
    "5" : b5,
    "6" : b6,
    "7" : b7,
    "8" : b8,
    "9" : b9,
    "10" : b10,
    "11" : b11,
    "12" : b12
}

# DICTIONARY OF EACH ROW FOR EACH DICTIONARY OF A GIVEN ROW
Rows = {
    "A" : A_Row,
    "B" : B_Row
}

# FOR USE WITH AVERAGING VALUES
def appendInfo(input_arr, tmp_arr):
    for v in self.tmp_arr:
        # Check to see if temporary array has been filled
        if (len(input_arr) == 0):
            input_arr = copy.deepcopy(tmp_arr)
            # Else, append new values to temporary array
        else:
            for i in range (0, len(input_arr) - 1):
                input_arr[i][3] += tmp_arr[i][3]
            return input_arr

def gatherLoop(EarliestDate):
    rack_dic = {}
    row_dic = {}
    data_arr = []
    tmp_arr =  []
    # GATHER INFO FROM EACH ROW
    start = time()
    date = getDateTime()
    for row_name, row_val in Rows.items():
        # For each rack
        for rack_name, rack_val in row_val.items():
            # For each class 
            for d_obj in rack_val[1]:
                # Returns reading_name, reading_value
                tmp_arr.append(d_obj.Get())
            rack_dic[rack_name] = {rack_val[0]:copy.deepcopy(tmp_arr)}
            del tmp_arr[:]
        row_dic[row_name] = [rack_val[0],copy.deepcopy(rack_dic)]
        rack_dic.clear()
    # Store Data
    storeData(row_dic, date)
    # Delete all old data
    deleteOldData(EarliestDate)
    rack_dic.clear()
    # Wait for interval to end
    while(time() - start < interval):
        sleep(.1)

# Main Loop
def main():
    act_int = interval
    eprint (getDateTime(), "\nStarting Data Center Monitoring...\n")
    print ("Interval Time :", act_int, " sec /", round((act_int/60.0),2) ," min")
    EarliestDate = getEarliestDate()
    print ("Oldest Date       :", EarliestDate)
    while True:
	execfile('/root/dcm/conf.py')
        gatherLoop(EarliestDate)

main()
