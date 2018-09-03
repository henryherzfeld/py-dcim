# ARRAY OF ALL OIDS FOR A GIVEN RACK
# [dbname, [device classes]]
a2 = ["ups1", [
    Ups1('10.15.30.184')
]]
a3 =["ups2", [
    Ups2('10.15.30.186')
]]
a4 =["rpdu", [
    RackPdu_a('10.15.30.151'),
    RackPdu_b('10.15.31.154'),
    TempSensor('3406802758', '10.15.30.193'),
    ACRackTemp("10.15.31.155", 3),
    HumiSensor('3273299739', '10.15.30.193')
]]
a5 =["rpdu", [
    RackPdu_a('10.15.30.189'),
    RackPdu_b('10.15.31.154'),
    ACRackTemp("10.15.31.155", 2),
    TempSensor('1619732064', '10.15.30.193'),
    HumiSensor('1974269701', '10.15.30.193')
]]
a6 =["inlinerp", [
    AC('10.15.31.155')
]]
a7 =["rpdu", [
    RackPdu_a('10.15.30.156'),
    RackPdu_b('10.15.30.157'),
    ACRackTemp("10.15.31.155", 1),
    TempSensor('2628357572', '10.15.30.193'),
    HumiSensor('2804425567', '10.15.30.193')
]]
a8 =["rpdu", [
    RackPdu_a('10.15.30.158'),
    RackPdu_b('10.15.30.159'),
    TempSensor('1665932156', '10.15.30.193'),
    HumiSensor('1668196833', '10.15.30.193')
]]
a9 =["rpdu", [
    RackPdu_a('10.15.30.160'),
    RackPdu_b('10.15.30.161'),
    ACRackTemp("10.15.30.162", 3),
    TempSensor('3328914949', '10.15.30.193'),
    HumiSensor('581338442', '10.15.30.193')
]]
a10 =["inlinerp", [

    AC('10.15.30.162')
]]
a11 =["rpdu", [
    RackPdu_a('10.15.30.163'),
    RackPdu_b('10.15.30.164'),
    ACRackTemp('10.15.30.162', 2),
    TempSensor('242089423', '10.15.30.193'),
    HumiSensor('338404919', '10.15.30.193')
]]
a12 =["rpdu", [
    RackPdu_a('10.15.30.165'),
    RackPdu_b('10.15.30.166'),
    ACRackTemp('10.15.30.162', 1),
    TempSensor('2716713264', '10.15.30.193'),
    HumiSensor('976244450', '10.15.30.193')
]]

b2 =["ups1", [
    Ups1('10.15.30.185')
]]
b3 =["ups2", [
    Ups2('10.15.30.183')
]]
b4 =["rpdu", [
    RackPdu_a('10.15.30.167'),
    RackPdu_b('10.15.30.168'),
    ACRackTemp('10.15.30.171', 3),
    TempSensor('3406802758', '10.15.30.191'),
    HumiSensor('3273299739', '10.15.30.191')
]]
b5 =["rpdu", [
    RackPdu_a('10.15.30.169'),
    RackPdu_b('10.15.30.200'),
    ACRackTemp('10.15.30.171', 2),
    TempSensor('1619732064', '10.15.30.191'),
    HumiSensor('1974269701', '10.15.30.191')
]]
b6 =["inlinerp", [
    AC('10.15.30.171')
]]
b7 =["rpdu", [
    RackPdu_a('10.15.30.172'),
    RackPdu_b('10.15.30.173'),
    TempSensor('2628357572', '10.15.30.191'),
    HumiSensor('2804425567', '10.15.30.191')
]]
b8 =["rpdu", [
    RackPdu_a('10.15.30.174'),
    RackPdu_b('10.15.30.175'),
    ACRackTemp('10.15.30.171', 1),
    TempSensor('1665932156', '10.15.30.191'),
    HumiSensor('1668196833', '10.15.30.191')
]]
b9 =["rpdu", [
    RackPdu_a('10.15.30.176'),
    RackPdu_b('10.15.30.177'),
    ACRackTemp('10.15.30.178', 3),
    TempSensor('3328914949', '10.15.30.191'),
    HumiSensor('581338442', '10.15.30.191')
]]
b10 =["inlinerp", [
    AC('10.15.30.178')
]]
b11 =["rpdu", [
    RackPdu_a('10.15.30.179'),
    RackPdu_b('10.15.30.180'),
    ACRackTemp('10.15.30.178', 2),
    TempSensor('242089423', '10.15.30.191'),
    HumiSensor('338404919', '10.15.30.191')
]]
b12 =["rpdu", [
    RackPdu_a('10.15.30.181'),
    RackPdu_b('10.15.30.182'),
    ACRackTemp('10.15.30.178', 1),
    TempSensor('2716713264', '10.15.30.191'),
    HumiSensor('976244450', '10.15.30.191')
]]

# DICTIONARY OF EACH RACK NUMBER FOR A GIVEN RACK ARRAY 
A_Row = {
    "2" : a2,
    "3" : a3,
    "4" : a4,
    "5" : a5,
    "6" : a6,
    "7" : a7,
    "8" : a8,
    "9" : a9,
    "10" : a10,
    "11" : a11,
    "12" : a12
}

B_Row = {
    "2" : b2,
    "3" : b3,
    "4" : b4,
    "5" : b5,
    "6" : b6,
    "7" : b7,
    "8" : b8,
    "9" : b9,
    "10" : b10,
    "11" : b11,
    "12" : b12
}

# DICTIONARY OF EACH ROW FOR EACH DICTIONARY OF A GIVEN ROW
Rows = {
    "A" : A_Row,
    "B" : B_Row
}