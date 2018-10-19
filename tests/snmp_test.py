import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

import pytest
import dcim.configuration as conf
import dcim.snmp as snmp
import dcim.core as core


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
    engine = snmp.SNMPEngine(core.get_snmp_targets())

    assert engine

def test_snmp_enqueue():
    engine = snmp.SNMPEngine(core.get_snmp_targets())
    engine.enqueue_requests()

    assert engine.requests


def test_snmp_single():
    engine = snmp.SNMPEngine(core.get_snmp_targets())
    result = engine.test()
    print(result)
    assert 'something' in result
