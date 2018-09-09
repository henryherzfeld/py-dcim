from dcim import core, transaction
from time import time
import asyncio


def main():

    # grabbing chron config from yaml in package root
    config_chron = core.get_config('chron')

    # build snmp target dictionary from equipment profiles
    snmp_targets = core.get_snmp_targets()

    # create

    while True:
        start = time()

        # collecting data from snmp target dictionary
        io = core.process_targets(snmp_targets)

        # storing snmp data dictionary
        transaction.store_snmp_data(snmp_data)

        # waiting for specified collection interval value
        core.wait(start, config_chron['COLLECT_INTERVAL'])
