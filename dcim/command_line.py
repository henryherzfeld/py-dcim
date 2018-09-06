import mysql
import dcim

def scaffold():
  data = dcim.extract_config()
  dcim.create_connection(data)


def run():
    dcim.main()