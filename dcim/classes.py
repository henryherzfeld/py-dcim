import dcim.builder as build
from collections import defaultdict
from dcim.configuration import get_config


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
            oid_obj_array = build.oids(oid_array)

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
        self.snmp_requests = build.snmp_requests(self.oid_array)
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
