import dcim
from dcim import core, transaction


def scaffold():

    transaction.create_connection()


def run():

    dcim.main()
