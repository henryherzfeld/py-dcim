import copy
import netsnmp
from time import time
from time import sleep
import sys
from datetime import datetime
import yaml
from dcim import transaction


# accepts a key string, if object matches key, returns it
def get_config(key):
    conf = yaml.load(open("conf.yaml"))
    if conf[key]:
        return conf[key]


def get_snmp_target():
    return 0


# Prints messages to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# Calls snmp_get and returns values
def snmp_get(ip, oid, div):
    session = netsnmp.Session(DestHost=ip, Version=2, Community=comm)
    vars = netsnmp.VarList(netsnmp.Varbind(oid))
    v = session.get(vars)
    if str(v[0]) == '-1':
        eprint(get_date_time(), "OID not used on device", oid, "from IP", ip, sep=": ")
        sys.exit("OID not used on device")
    elif v[0] == '':
        eprint(get_date_time(), "Error in OID", oid, "from IP", ip, sep=": ")
        return ''
    else:
        try:
                ret = round((float(v[0])/div),1)
                return str(ret)
        except:
                if v[0] == None:
                    return
                else:
                    eprint(get_date_time(), "Unknown Error ", v[0], sep=": ")


# called by the classes, will return a dictionary of
# a walk through of each oid and its date-time stamp
def oid_walk(oid_arr, ip, sensor):
    vals = []
    for v in oid_arr:
        o = ''.join([v[1], sensor])
        #print v
        val = snmp_get(ip, o, v[2])
        if val is not None:
            vals.append([v[0], val])
    return vals


# accepts a rack array of equipment classes, initializes them, stores them, deletes, returns
def process_rack(rack_profile):
    tmp_arr =[]

    # For each class
    for equipment in rack_profile[1]:

        # fills tmp_arr with val_arr from oid_walk call from each d_obj.get
        tmp_arr.append(equipment.get())

    rack_readings = { rack_profile[0] : copy.deepcopy(tmp_arr) }
    del tmp_arr[:]
    return rack_readings


# return date and time in proper format
def get_date_time():
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dt


# wait for specified (conf.yaml) interval value
def wait(start, interval):
    while time() - start < interval:
        sleep(.1)


# FOR USE WITH AVERAGING VALUES
def append_info(input_arr, tmp_arr):
    for v in tmp_arr:
        # Check to see if temporary array has been filled
        if len(input_arr) == 0:
            input_arr = copy.deepcopy(tmp_arr)

        # Else, append new values to temporary array
        else:
            for i in range(0, len(input_arr) - 1):
                input_arr[i][3] += tmp_arr[i][3]
            return input_arr


# hmm
def collect(rows):
    rack_dic = {}
    row_dic = {}

    for row_name, row_val in rows.items():

        # For each rack
        for rack_name, rack_val in row_val.items():

            # returns readings dictionary where dic[n] =
            # { rack_n_id : { rack_n_reading1_name : rack_n_reading1_val,
            #                 rack_n_reading2_name : ... }
            rack_dic[rack_name] = process_rack(rack_val)

        row_dic[row_name] = [
            rack_val[0],
            copy.deepcopy(rack_dic)
        ]
        rack_dic.clear()

    transaction.store_data(row_dic)


