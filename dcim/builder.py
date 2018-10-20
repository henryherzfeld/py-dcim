from pysnmp.hlapi.asyncio import (
    ObjectType,
    ObjectIdentity
)
from dcim.classes import (
     Oid,
     Equipment,
     Rack
)


# accepts config target data, returns array of Rack objects
# on init, ea rack object initializes their containing equipment
def racks(targets_blob):
    snmp_targets = []
    id = 0

    # getting individual equipment profile, row from configuration file
    for snmp_target_label, snmp_target in targets_blob.items():

        id += 1
        equipment = snmp_target['equipment']
        row = snmp_target['row']

        if equipment is None:
            print('Rack ' + id + 'has no equipment in configuration file')

        print('rack ' + row + str(id) + ' initialized')
        snmp_targets.append(Rack(id, equipment, row))

    return snmp_targets


# accepts config oid data relative to equipment type.
# returns array of Oid objects containing value and divisor
def oids(oid_array):
    oid_obj_array = []

    for oid_entry in oid_array:

        # handling layered dictionary and lists from config YAML
        oid_entry = oid_entry.popitem()[1]

        value = oid_entry['value']
        divisor = oid_entry['divisor']

        oid_obj = Oid(value, divisor)

        oid_obj_array.append(oid_obj)

    return oid_obj_array


# accepts an array of Oid objects and returns an array of SNMP objects (prepped for SNMPEngine)
# TODO: incorporate different MIBs (ie. APCPower-MIB) based upon equipment class
def snmp_requests(oids):
    snmp_obj_array = []

    for oid in oids:
        snmp_obj_array.append(ObjectType(ObjectIdentity('PowerNet-MIB', oid, '0')).loadMibs('C:/mibs'))

    return snmp_obj_array
