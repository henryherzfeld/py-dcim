from dcim.configuration import get_config
from collections import defaultdict


# accept an Equipment class, searches in configuration for oids matching Equipment type, binds to and returns Equipment
def build_equipment_snmp_data(equipment):
    oids = get_config('oids')[equipment.equipment_type]

    try:
        for oid_entry in oids:
            equipment.oid_array.append([oid_entry[oid]['value'] for oid in oid_entry])

    except KeyError as err:
        print("Key error: {0} ".format(err) + "for " + equipment.equipment_type)

    print(equipment.equipment_type + ' equipment\'s oid array built as: {0}'.format(equipment.oid_array))
    return equipment


# constructor accepts equipment array, processes each one to bind snmp data
class Rack:
    contains = []
    id = 0
    row = 0

    def __init__(self, id, rack_equipment, row):
        self.id = id
        self.row = row

        for equipment in rack_equipment:

            try:
                ip = equipment['ip']
                equipment_type = equipment['type']
            except KeyError as err:
                print("Key error: {0}".format(err) + 'not found in configuration file for Rack ' + self.id)

            else:
                configured_equipment = build_equipment_snmp_data(
                    Equipment(equipment_type, ip, row, id)
                )
                self.contains.append(configured_equipment)

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

    def __init__(self, equipment_type, ip, row, rack):
        self.equipment_type = equipment_type
        self.ip = ip
        self.oid_array = []
        self.rack = rack
        self.row = row
        sensor_id = ''
