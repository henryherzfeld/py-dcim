from pysnmp.hlapi.asyncio import (
    ObjectType,
    ObjectIdentity
)
from dcim.classes import (
     Oid,
     Equipment,
     Rack
)
from dcim.configuration import get_config


# accepts config target data, returns array of built
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


def oids(oid_array):
    oid_obj_array = []

    for oid_entry in oid_array:

        # handling layered dictionary and lists
        oid_entry = oid_entry.popitem()[1]

        value = oid_entry['value']
        divisor = oid_entry['divisor']

        oid_obj = Oid(value, divisor)
        print(oid_obj.get_oid())
        oid_obj_array.append(oid_obj)

    return oid_obj_array


# accepts an array of oid objects and
def snmp_objects(self, oids):
    var_binds = []
    #
    # for oid in oids:
    #     var_bind = ObjectType(ObjectIdentity('POWERNET-MIB', str(oid[0]), 0), 1)
    #
    #     var_binds.append(var_bind)
    # return var_binds

    for oid in oids:
        var_binds.append(ObjectType(ObjectIdentity('PowerNet-MIB', oid, '0')).loadMibs('C:/mibs'))

    return var_binds