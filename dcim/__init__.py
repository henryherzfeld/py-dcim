from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
from dcim.time import wait
from dcim.configuration import get_config
from dcim.snmp import SNMPEngine
from dcim.stream import StreamEngine
from time import time
import dcim.builder as build


def main():
    print("starting..")

    # collecting all data necessary for process loop
    config_chron = get_config('chron')
    targets_blob = get_config('targets')

    print('acquiring target table...')
    snmp_targets = build.racks(targets_blob)

    # initializing engines
    snmp_engine = SNMPEngine(snmp_targets)
    stream_engine = StreamEngine()

    while True:
        interval_start = time()

        snmp_engine.enqueue_requests()

        results = snmp_engine.process_requests()

        stream_engine.add(results)

        results.clear()

        wait(interval_start, config_chron['COLL_INTERVAL'])


