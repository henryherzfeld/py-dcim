from pysnmp.hlapi.asyncio import (
    ObjectType,
    ObjectIdentity
)
from collections import defaultdict
from dcim.configuration import get_config


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
        snmp_obj = ObjectType(ObjectIdentity(oid.get_oid()))
        snmp_obj_array.append(snmp_obj)


    return snmp_obj_array


# constructor accepts equipment array, processes each one to bind snmp data
class Rack:
    contains = []
    id = 0
    row = 0

    def __init__(self, id, rack_equipment, row):
        self.id = id
        self.row = row

        for equipment in rack_equipment:
            ip = equipment['ip']
            equipment_type = equipment['type']

            oid_array = get_config('oids')[equipment_type]
            oid_obj_array = oids(oid_array)

            self.contains.append(
                Equipment(
                    equipment_type,
                    ip,
                    row,
                    id,
                    oid_obj_array
                )
            )

    # builds a dictionary of lists where key is ip and value is list of each equipment's oid array
    def get_equipment_snmp_data(self):
        equipment_snmp_data = defaultdict(lambda: 0)

        for equipment in self.contains:
            entry = {equipment.ip: equipment.oid_array}
            equipment_snmp_data.update(entry)

        return equipment_snmp_data


# constructor assigns equipment type, ip, oids, rowm rack and (optionally) sensorid
class Equipment:
    equipment_type = ''
    ip = ''
    sensor_id = ''
    oid_array = []
    rack = 0
    row = 0

    def __init__(self, equipment_type, ip, row, rack, oid_obj_array):
        self.equipment_type = equipment_type
        self.ip = ip
        self.oid_array = oid_obj_array
        self.rack = rack
        self.row = row
        self.snmp_requests = snmp_requests(self.oid_array)
        self.sensor_id = ''


class Oid:
    value = 0
    divisor = 0

    def __init__(self, value, divisor):
        self.value = value
        self.divisor = divisor

    def get_oid(self):
        return self.value

    def get_divisor(self):
        return self.divisor
