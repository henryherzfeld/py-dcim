import mysql.connector
from mysql.connector import errorcode
from dcim.core import get_config


# connects mysql connector from conf.yaml database configuration
def create_connection():

    connection_auth = get_config('db')

    try:
        cnx = mysql.connector.connect(user=connection_auth['DB_USER'],
                                      database=connection_auth['DB_NAME'],
                                      use_pure=TRUE)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Incorrect database credentials in conf.yaml")
        else:
            print(err)

    else:
        cnx.close()


#
def store_snmp_target_data(snmp_target_data):


#
def initialize_database():
