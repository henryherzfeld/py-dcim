# Prints messages to stderr
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Calls snmpGet and returns values
def snmpGet(ip, oid, div):
    session = netsnmp.Session(DestHost=ip, Version=2, Community=comm)
    vars = netsnmp.VarList(netsnmp.Varbind(oid))
    v = session.get(vars)
    if(str(v[0]) == '-1'):
        eprint (getDateTime(), "OID not used on device", oid, "from IP", ip, sep=": ")
        sys.exit("OID not used on device")
    elif(v[0] == ''):
        eprint (getDateTime(), "Error in OID", oid, "from IP", ip, sep=": ")
        return ''
    else:
	try:
            ret = round((float(v[0])/div),1)
            return str(ret)
	except:
            if(v[0] == None):
                return
            else:
                eprint (getDateTime(), "Unknown Error ", v[0], sep=": ")

# Called by the classes, will return an dictionary of
# a walkthrough of each oid and its date-time stamp
def oidWalk(oid_arr, ip, sensor):
    vals = []
    for v in oid_arr:
        o = ''.join([v[1], sensor])
        #print v
        val = snmpGet(ip, o, v[2])
        if(val != None):
            vals.append([v[0], snmpGet(ip, o, v[2])])
    return (vals)

# Return date and time in proper format
def getDateTime():
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return dt

# Insert values into database
def insertData(device_dt, rack_id, device_id, device_arr):
    # Insert values into DB from row and rack id
    sql = "INSERT INTO " + device_id +  "(" + "rack_id, " + "reading_dt"
    val = " VALUES (" + "'" + rack_id + "', '" + device_dt + "'"
    for x in range(0, len(device_arr)):
        try:
            sql = sql + ", " + device_arr[x][0]
            val = val + ", '" + device_arr[x][1] + "'"
        except:
            eprint (getDateTime(), "Error in either device_arr[x][0]", device_arr[x][0], " or device_arr[x][1]", device_arr[x][1], sep=": ")
    sql = sql + ") "
    val = val + ");"
    sql = sql + val
    try:
        c.execute(sql)
        conn.commit()
    except:
        eprint (getDateTime(), "Error in SQL Insert", sql, sep=": ")

# Get array thats stored all information for storage
# arr[row_id, rack_number, reading_name, reading_value, date-time]
def storeData(row_dic, date_dt):
    for row_id, rack_dic in row_dic.items():
        for rack_number, device_arr_dic in rack_dic[1].items():
            values = []
            for device_id, device_arr_arr in device_arr_dic.items():
                # Get database row_id
                sql=''.join(["SELECT rack_id FROM rack WHERE row_id='", row_id, "' AND rack_number='", rack_number, "'"])
                try:
                    c.execute(sql)
                    conn.commit()
                except:
                    eprint (getDateTime(), "Error in SQL select", sql, sep=": ")
                rid = c.fetchall()
                rack_id = str(rid[0][0])
                # Should only return one row
                if(len(rid) != 1):
                    eprint (getDateTime(), "Multiple rows on rack_id query", sql, sep=": ")
                    break
                else:
                    for device_arr in device_arr_arr:
                        for v in device_arr:
                            # Combine each device in a rack into one array
                            values.append(v)

                # Insert combined rack into database
                insertData(date_dt, rack_id, device_id, values)                   


# Returns the earliest date from 'reading' table
def getEarliestDate():
    sql = "SELECT min(mx) FROM (SELECT max(reading_dt) AS `mx` FROM ups1 UNION SELECT max(reading_dt) AS `mx` FROM ups2 UNION SELECT max(reading_dt) AS `mx` FROM rpdu UNION SELECT max(reading_dt) AS `mx` FROM inlinerp) AS t1;"
    try:
        c.execute(sql)
        conn.commit()
        ed = c.fetchall()
	if(ed[0][0]==None):
            print ("No Earliest Record")
	    dt = getDateTime()
	    return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        else:
            return ed[0][0]
    except:
        eprint (getDateTime(), "Error in SQL select (getting oldest date)", sql, sep=": ")

# Deletes all data that is over 2 years old
def deleteOldData(EarliestDate):
    tables = ["rpdu", "ups1", "ups2", "inlinerp"]
    mi = EarliestDate.month + monthinterval
    if(mi > 12):
        dtcmp = EarliestDate.replace(month=(mi%12), year=(EarliestDate.year-1))
    else:
        dtcmp = EarliestDate.replace(month=(mi))

    if(datetime.now() <= dtcmp):
        return

    for v in tables:
        sql = ''.join(["DELETE FROM ",v," WHERE reading_dt < DATE_SUB(CURDATE(), INTERVAL ", str(monthinterval), " MONTH);"])
        try:
            print (sql)
            c.execute(sql)
            conn.commit()
        except:
            eprint (getDateTime(), "Error in SQL (deleting old data)", sql, sep=": ")


# FOR USE WITH AVERAGING VALUES
def appendInfo(input_arr, tmp_arr):
    for v in self.tmp_arr:
        # Check to see if temporary array has been filled
        if (len(input_arr) == 0):
            input_arr = copy.deepcopy(tmp_arr)
            # Else, append new values to temporary array
        else:
            for i in range (0, len(input_arr) - 1):
                input_arr[i][3] += tmp_arr[i][3]
            return input_arr

def gatherLoop(EarliestDate):
    rack_dic = {}
    row_dic = {}
    data_arr = []
    tmp_arr =  []
    # GATHER INFO FROM EACH ROW
    start = time()
    date = getDateTime()
    for row_name, row_val in Rows.items():
        # For each rack
        for rack_name, rack_val in row_val.items():
            # For each class 
            for d_obj in rack_val[1]:
                # Returns reading_name, reading_value
                tmp_arr.append(d_obj.Get())
            rack_dic[rack_name] = {rack_val[0]:copy.deepcopy(tmp_arr)}
            del tmp_arr[:]
        row_dic[row_name] = [rack_val[0],copy.deepcopy(rack_dic)]
        rack_dic.clear()
    # Store Data
    storeData(row_dic, date)
    # Delete all old data
    deleteOldData(EarliestDate)
    rack_dic.clear()
    # Wait for interval to end
    while(time() - start < interval):
        sleep(.1)