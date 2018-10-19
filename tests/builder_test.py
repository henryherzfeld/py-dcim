import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import dcim.builder as build
import dcim.configuration as config
from dcim.classes import (
     Oid,
     Equipment,
     Rack
)


def test_build_equipment():
    targets_blob = config.get_config('targets')

    snmp_targets = build.racks(targets_blob)

    for target in snmp_targets:
        assert type(target) is Rack

        for equipment in target.contains:
            assert type(equipment) is Equipment

            for oid in equipment.oid_array:
                assert type(oid) is Oid
