from dcim import core, transaction
from time import time


def main():

    chron = core.get_config('chron')

    objects = core.get_snmp_target()
    start = time()

    while True:

        core.collect(objects)
        transaction.store_data()
        core.wait(start, chron['COLLECT_INTERVAL'])


