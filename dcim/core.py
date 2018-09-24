import copy
from time import time
from time import sleep
from yaml import load
from dcim import engine


# accepts a key string, if object matches key, returns it
def get_config(key):
    conf = load(open("conf.yaml"))
    if conf[key]:
        return conf[key]


# this is where we build an array of all targets
def get_snmp_targets():
    snmp_targets[] = equipment.json
    return snmp_targets[]


#
def process_snmp_target(snmp_target):
    snmp_target_data = []

    for equipment in snmp_target.contains:
        snmp_target_data.append((engine.async_process_equipment(equipment)))

    return snmp_target_data


# wait for specified (conf.yaml) interval value
def wait(start, interval):
    while time() - start < interval:
        sleep(.1)
