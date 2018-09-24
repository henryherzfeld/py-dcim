from dcim import core, transaction
from time import time


def main():

    # collecting all data necessary for process loop
    config_chron = core.get_config('chron')
    snmp_targets = core.get_snmp_targets()
    snmp_target_data = {}
    start = time()

    while True:
        interval_start = time()

        for snmp_target in snmp_targets:
            snmp_target_data[snmp_target.name] = core.process_snmp_target(snmp_target)

        transaction.store_snmp_target_data(snmp_target_data)

        core.wait(interval_start, config_chron['COLLECT_INTERVAL'])
