import MySQLdb

# Community string for SNMP
comm='APC1130fau'

# Interval to delete data (in months)
monthinterval = 4

# Total time delay in seconds between pushing info
interval = 120

# MYSQL connection info
server='localhost'
usr='root'
passwd='Ev7^b33nz04Spm'
db='dcm'
usrdb='$'.join([usr,db])

conn = MySQLdb.connect(server,usr,passwd,db)
c=conn.cursor()

# UPS OIDS USED
# [name, oid, divisor]            
upsOids = [
    ("nominal_voltage",  'upsAdvBatteryNominalVoltage.0', 1),
    ("input_frequency", "upsAdvInputFrequency.0", 1),
    ("output_frequency", "upsAdvOutputFrequency.0", 1),
    ("input_voltage_1_phase_1", "upsPhaseInputVoltage.1.1.1", 1),
    ("input_voltage_1_phase_2", "upsPhaseInputVoltage.1.1.2", 1),
    ("input_voltage_1_phase_3", "upsPhaseInputVoltage.1.1.3", 1),
    ("input_voltage_2_phase_1", "upsPhaseInputVoltage.2.1.1", 1),
    ("input_voltage_2_phase_2", "upsPhaseInputVoltage.2.1.2", 1),
    ("input_voltage_2_phase_3", "upsPhaseInputVoltage.2.1.3", 1),
    ("input_current_1_phase_1", "upsPhaseInputCurrent.1.1.1", 10),
    ("input_current_1_phase_2", "upsPhaseInputCurrent.1.1.2", 10),
    ("input_current_1_phase_3", "upsPhaseInputCurrent.1.1.3", 10),
    ("output_current_phase_1", "upsPhaseOutputCurrent.1.1.1", 10),
    ("output_current_phase_2", "upsPhaseOutputCurrent.1.1.2", 10),
    ("output_current_phase_3", "upsPhaseOutputCurrent.1.1.3", 10),
    ("output_voltage_phase_1", "upsPhaseOutputVoltage.1.1.1", 1),
    ("output_voltage_phase_2", "upsPhaseOutputVoltage.1.1.2", 1),
    ("output_voltage_phase_3", "upsPhaseOutputVoltage.1.1.3", 1),

]

# Main Pdu (UPS2) OIDS
# [name, oid, divisor]            
ups2Oids = [
    ("output_frequency", 'xPDUSystemOutputFrequency.0',10),
    ("input_voltage_ltol_phase_1", 'xPDUMainInputVoltageLtoL.1',10),
    ("input_voltage_ltol_phase_2", 'xPDUMainInputVoltageLtoL.2',10),
    ("input_voltage_ltol_phase_3", 'xPDUMainInputVoltageLtoL.3',10),
    ("output_voltage_ltol_phase_1", 'xPDUSystemOutputVoltageLtoL.1',10),
    ("output_voltage_ltol_phase_2", 'xPDUSystemOutputVoltageLtoL.2',10),
    ("output_voltage_ltol_phase_3", 'xPDUSystemOutputVoltageLtoL.3',10),
    ("output_voltage_lton_phase_1", 'xPDUSystemOutputVoltageLtoN.1',10),
    ("output_voltage_lton_phase_2", 'xPDUSystemOutputVoltageLtoN.2',10),
    ("output_voltage_lton_phase_3", 'xPDUSystemOutputVoltageLtoN.3',10),
    ("output_current_ltol_phase_1", 'xPDUSystemOutputPhaseCurrent.1',10),
    ("output_current_ltol_phase_2", 'xPDUSystemOutputPhaseCurrent.2',10),
    ("output_current_ltol_phase_3", 'xPDUSystemOutputPhaseCurrent.3',10),
    ("output_power_ltol_phase_1", 'xPDUSystemOutputPower.1',.01),
    ("output_power_ltol_phase_2", 'xPDUSystemOutputPower.2',.01),
    ("output_power_ltol_phase_3", 'xPDUSystemOutputPower.3',.01),
    ("output_power_factor_ltol_phase_1", 'xPDUSystemOutputPowerFactor.1',100),
    ("output_power_factor_ltol_phase_2", 'xPDUSystemOutputPowerFactor.2',100),
    ("output_power_factor_ltol_phase_3", 'xPDUSystemOutputPowerFactor.3',100)
]

# Rack Pdu OIDS
# [name, oid, divisor]            
rackPduOids = [ 
    ("power", 'rPDUIdentDevicePowerWatts.0',1),
    ("power_factor", 'rPDUIdentDevicePowerFactor.0',1000),
    ("ltol_voltage", 'rPDUIdentDeviceLinetoLineVoltage.0',1)
]

# AC/InlineRP OIDS
# [name, oid, divisor]            
acOids = [
    ("rack_inlet_temp", 'airIRRP100UnitStatusRackInletTempMetric.0',10),
    ("supply_air_temp", 'airIRRP100UnitStatusSupplyAirTempMetric.0',10),
    ("return_air_temp", 'airIRRP100UnitStatusReturnAirTempMetric.0',10),
    ("compressor_drive_power", 'airIRRP100UnitStatusCompressorDrivePower.0',.01),
    ("compressor_drive_voltage", 'airIRRP100UnitStatusCompressorDriveVoltage.0',10),
    ("compressor_drive_current", 'airIRRP100UnitStatusCompressorDriveCurrent.0',10)
]

# TempSensor OIDS
# [name, oid, divisor] 
tempSensorOids = [
    ("temp", 'tempSensorValue.', 10)
]

# Humidity Sensor OIDS
# [name, oid, divisor]            
humiSensorOids = [
    ("humi", 'humiSensorValue.', 10)
]

# Dew Point OIDS
# [name, oid, divisor]            
dewPointOids = [
    ("dew", 'dewPointSensorValue.',10)
]
