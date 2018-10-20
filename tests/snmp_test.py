import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import dcim.configuration as conf
import dcim.snmp as snmp
import dcim.builder as build


def test_targets_config():
    config = conf.get_config('targets')

    for target in config:
        for equipment in config[target]['equipment']:

            assert 'ip' in equipment
            assert 'type' in equipment


def test_oids_config():
    config = conf.get_config('oids')

    for equipment in config:
        for oid_entry in config[equipment]:
            for label in oid_entry:

                assert label


def test_snmp_constructor():
    engine = snmp.SNMPEngine(build.racks(conf.get_config('targets')))

    assert engine


def test_snmp_enqueue():
    engine = snmp.SNMPEngine(build.racks(conf.get_config('targets')))
    engine.enqueue_requests()

    assert engine.requests


def test_snmp_single():
    engine = snmp.SNMPEngine(build.racks(conf.get_config('targets')))
    result = engine.test()

    assert 'something' in result
