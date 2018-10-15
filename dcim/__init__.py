from dcim.core import get_snmp_targets
from dcim.configuration import get_config
from dcim.snmp import SNMPEngine
from dcim.stream import StreamEngine
from time import time
from collections import defaultdict


def main():
    print("starting..")

    # collecting all data necessary for process loop
    config_chron = get_config('chron')

    print('acquiring target table...')
    snmp_targets = get_snmp_targets()

    snmp_target_data = defaultdict(lambda: 0)
    start = time()

    # initializing engines
    engine = SNMPEngine(snmp_targets)
    stream_engine = StreamEngine()

    while True:
        interval_start = time()

        engine.enqueue_requests()

        results = engine.process_requests()

        stream_engine.add(results)

        core.wait(interval_start, config_chron['COLL_INTERVAL'])
