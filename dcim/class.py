from dcim.core import oid_walk, get_snmp_target


# Class with regards to all UPS devices
class Ups1:
    ip = ''

    def __init__(self, ip):
        self.ip = ip

    # Go through each OID and return the respective value
    def get(self):
        return oid_walk(upsOids, self.ip,  '')


# Power Distribution Unit
class Ups2:
    ip = ''

    def __init__(self, ip):
        self.ip = ip

    def get(self):
        return oid_walk(ups2Oids, self.ip,  '')


class RackPdu_a:
    ip = ''
    oids = []
    for x in range(0, len(rackPduOids)):
        oids.append(["pdua_" + rackPduOids[x][0], rackPduOids[x][1], rackPduOids[x][2]])

    def __init__(self, ip):
        self.ip = ip

    def get(self):
        return oid_walk(self.oids, self.ip,  '')


class RackPdu_b:
    ip = ''
    oids = []

    for x in range(0, len(rackPduOids)):
        oids.append(["pdub_" + rackPduOids[x][0], rackPduOids[x][1], rackPduOids[x][2]])

    def __init__(self, ip):
        self.ip = ip

    def get(self):
        return oid_walk(self.oids, self.ip,  '')


# OID is defined by initialization
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


class AC:
    ip = ''

    def __init__(self, ip):
        self.ip = ip

    def get(self):
        return oid_walk(acOids, self.ip,  '')


class TempSensor:
    ip = ''
    sensor = ''

    def __init__(self, sensor, ip):
        self.sensor = sensor
        self.ip = ip

    def get(self):
        return oid_walk(tempSensorOids, self.ip,  self.sensor)


class HumiSensor:
    ip = ''
    sensor = ''

    def __init__(self, sensor, ip):
        self.sensor = sensor
        self.ip = ip

    def get(self):
        return oid_walk(humiSensorOids, self.ip,  self.sensor)
