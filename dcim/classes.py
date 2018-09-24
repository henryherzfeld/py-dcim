from dcim.core import get_config


#
def build_oid(equipment):

    for x in range(0, len(equipment.oid_array)):
        equipment.oid_array.append([
                                    equipment.oid_array[x][0],
                                    equipment.oid_array[x][1]
                                   ])
        return equipment


#
def build_equipment_snmp_data(equipment):

    if equipment.equipment_type is not None:

        equipment.oid_array = build_oid(
            get_config('oids')[equipment.equipment_type]
        )

        if equipment.sensor_id is not None:
            equipment.oid_array.append(equipment.sensor_id)

        return equipment

    else:
        return


#
class Rack:
    contains = []
    id = 0
    row = 0

    def __init__(self, id, rack_equipment, row):
        self.id = id
        self.row = row

        # - racks:
        #       - 1:
        #         row: a
        #         equipment:
        #             - ups:
        #                   ip: 10.15.30.184

        # model after above yaml format

        #  {
        #   1: {
        #        row: a,
        #        equipment: {
        #            ups: {
        # `              ip: 10.15.30.184
        #                }
        #            }
        #        }
        #   2: {
        #        ...
        # }

        for equipment in range(0, len(rack_equipment)):
            configured_equipment = build_equipment_snmp_data(equipment)
            self.contains.append(configured_equipment)


#
class Equipment:
    equipment_type = ''
    ip = ''
    sensor_id = ''
    oid_array = []

    def __init__(self, type):
