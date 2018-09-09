import mysql.connector
from mysql.connector import errorcode
from dcim.core import eprint, get_config, get_date_time


class TransactionHandler:
    y = 10


# accepts db config object, connects using it
def create_connection():

    cnx_auth = get_config('db')
    try:
        cnx = mysql.connector.connect(user=cnx_auth['DB_USER'],
                                      database=cnx_auth['DB_NAME'])
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


# Insert values into database
def insert_data(device_dt, rack_id, device_id, device_arr):
    # Insert values into DB from row and rack id
    sql = "INSERT INTO " + device_id +  "(" + "rack_id, " + "reading_dt"
    val = " VALUES (" + "'" + rack_id + "', '" + device_dt + "'"
    for x in range(0, len(device_arr)):
        try:
            sql = sql + ", " + device_arr[x][0]
            val = val + ", '" + device_arr[x][1] + "'"
        except:
            eprint(get_date_time(), "Error in either device_arr[x][0]", device_arr[x][0], " or device_arr[x][1]", device_arr[x][1], sep=": ")
    sql = sql + ");"
    val = val + ");"
    sql = sql + val
    try:
        c.execute(sql)
        conn.commit()
    except:
        eprint(get_date_time(), "Error in SQL Insert", sql, sep=": ")


# get array and store into MySQL
# arr[row_id, rack_number, reading_name, reading_value, date-time]
def store_row(row, row_id):
    for rack_number, device_arr_dic in row.items():
        values = []
        for device_id, device_arr_arr in device_arr_dic.items():

            # Get database row_id
            sql=''.join(["SELECT rack_id FROM rack WHERE row_id='", row_id, "' AND rack_number='", rack_number, "'"])
            try:
                c.execute(sql)
                conn.commit()
            except:
                eprint (get_date_time(), "Error in SQL select", sql, sep=": ")
            rid = c.fetchall()
            rack_id = str(rid[0][0])
            # Should only return one row
            if(len(rid) != 1):
                eprint (get_date_time(), "Multiple rows on rack_id query", sql, sep=": ")
                break
            else:
                for device_arr in device_arr_arr:
                    for v in device_arr:
                        # Combine each device in a rack into one array
                        values.append(v)

            # Insert combined rack into database
            insert_data(date_dt, rack_id, device_id, values)


# accepts a rows 'dictionary' object, stores them
def store_snmp_data(rows):
    for row in rows:
        store_row(row)