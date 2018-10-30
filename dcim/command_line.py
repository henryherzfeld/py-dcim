import pytest
from dcim import main

# all command line entry points as specified in setup.py are called here


def run():
    print("starting..")
    main.run()


def test():
    print("running tests..")
    pytest.main()
