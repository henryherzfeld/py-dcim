from time import time, sleep
from dcim.classes import Rack
from dcim.configuration import get_config


# this is where we build an array of all targets
def get_snmp_targets():
    snmp_targets = []
    id = 0

    snmp_targets_blob = get_config('targets')

    # getting individual equipment profile, row from configuration file
    for snmp_target_label, snmp_target in snmp_targets_blob.items():

        id += 1
        equipment = snmp_target['equipment']
        row = snmp_target['row']

        if equipment is None:
            print('Rack ' + id + 'has no equipment in configuration file')

        print('rack ' + row + str(id) + ' initialized')
        snmp_targets.append(Rack(id, equipment, row))

    return snmp_targets


# wait for specified (conf.yaml) interval value
def wait(start, interval):
    print('waiting {0} seconds'.format(interval-(time()-start)))
    while time() - start < interval:
        sleep(.1)
