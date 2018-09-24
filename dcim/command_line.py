import json
from dcim.transaction import create_connection
from dcim.core import get_config
# all command line entry points as specified in setup.py are called here


# command for opening database connections from config
def scaffold():

    create_connection()

    get_config('')


# command for starting snmp processing
def run():
    dcim.main()
