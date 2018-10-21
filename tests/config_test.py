import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
import dcim.configuration as conf
from collections import defaultdict


def test_config_targets():
    config = conf.get_config('targets')

    assert type(config) is defaultdict


def test_config_oids():
    config = conf.get_config('oids')

    assert type(config) is defaultdict

    for equipment in config.items():
        assert type(equipment) is tuple