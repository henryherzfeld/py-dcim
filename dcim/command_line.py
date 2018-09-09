import dcim
import json
from dcim import core, transaction
# all command line entry points as specified in setup.py are called here


# command for opening database connections from profile.JSON
def scaffold():
    transaction.create_connection()

    json.load()

# command for starting snmp processing
def run():
    dcim.main()
