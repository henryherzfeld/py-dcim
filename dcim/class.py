from dcim.core import oid_walk, get_snmp_targets

# checks container's type and pulls relevant
def get_contents(container):


    if container.type == 'row':

        return data


class Row:
    type = 'row'
    contains = []

    def __init__(self, contains, type):
        self.type = 'row'
        self.contains = get_contents(self)



class AC:
class UPS:
    ip = ''

    def __init__(self, ip):
        self.ip = ip

    # Go through each OID and return the respective value
    def get(self):
        return oid_walk(upsOids, self.ip,  '')

class Sensor:
    class TempSensor:
        ip = ''
        sensor = ''

        def __init__(self, sensor, ip):
            self.sensor = sensor
            self.ip = ip

        def get(self):
            return oid_walk(tempSensorOids, self.ip, self.sensor)



class RackPDU:
    ip = ''
    oids = []

    for x in range(0, len(rackPduOids)):
        oids.append(["pdu" +  + rackPduOids[x][0], rackPduOids[x][1], rackPduOids[x][2]])

    def __init__(self, ip):
        self.ip = ip

    def get(self):
        return oid_walk(self.oids, self.ip,  '')



class ACRackTemp:
    # [name, oid, divisor]            
    oids = []
    ip = ''

    def __init__(self, ip, rid):
        self.ip = ip
        rid = int(rid)

        if rid > int(3) or rid < int(1):
            sys.exit("rid not equal to 1, 2, or 3")

        tmp = 'airIRRP100UnitStatusRackInletTemperature' + str(rid) + 'Metric.0'
        tmp2 = "temp2"
        self.oids = [(tmp2, tmp, 10)]

    def get(self):
        return oid_walk(self.oids, self.ip,  '')






