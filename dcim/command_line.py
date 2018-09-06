import mysql
import dcim

def bootstrap():
  data = dcim.extract_config()
  dcim.create_connection(data)


def run():
    dcim.main()