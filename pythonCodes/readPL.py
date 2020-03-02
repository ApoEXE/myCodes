#Array on PLFDataLog all int but 4 bytes int
#timeStamp  8 bytes ms
# Tonnage   4 bytes * 1000
# FilterTon 4 bytes * 1000
# speed     4 bytes * 1000
# state     4 bytes ->
#define STATE_UNKNOWN       0
#define STATE_EMPTY_STOP    1
#define STATE_EMPTY_MOVE    2
#define STATE_LOADING       3
#define STATE_LOADED_MOVE   4
#define STATE_LOADED_STOP   5
#define STATE_DUMPING       6
#row two of the sql output is binary data
import sqlite3
from sqlite3 import Error
import csv
import matplotlib.pyplot as plt
import keyword as kb
from drawnow import drawnow
import time
DB="PLFDataLog"
#path_to_DB = "/Users/jav/Desktop/ControlBox_FC107_30_01_20.db"
path_to_DB = "/Users/jav/Desktop/ControlBox.db"
_ton = 0
_status = ''
_ton_old = 0
_slope = 0
_status_old = ''
_time = []
_raw_ton =[]
_filt_ton =[]
_filt_status =[]
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
 
def payload_status(conn):

    """
    Gathers the raw data of payload
    speed, and time
    Filters out payload and status
    :param conn: the Connection object
    :return:
    """
    time_old = 0
    global _status_old
    cur = conn.cursor()
    cur.execute("SELECT * FROM  PLFDataLog")
    rows = cur.fetchall()

    for row in rows:
        status = (row[2][23] << 24)|(row[2][22] << 16)|(row[2][21] << 8)|(row[2][20])
        speed = (row[2][19] << 24) | (row[2][18] << 16) | (row[2][17] << 8) | (row[2][16])
        filter = (row[2][15] << 24) | (row[2][14] << 16) | (row[2][13] << 8) | (row[2][12])
        ton = (row[2][11] << 24) | (row[2][10] << 16) | (row[2][9] << 8) | (row[2][8])
        time_stamp = (row[2][7] << 56) | (row[2][6] << 48) | (row[2][5] << 40) | (row[2][4]|row[2][23] << 32) | (row[2][3] << 24) | (row[2][2] << 16) | (row[2][1])<<8 |(row[2][0])
        if status == 0:
            st_status = 'STATE_UNKNOWN'
        elif status ==1:
            st_status = 'EMPTY_STOP'
        elif status ==2:
            st_status = 'EMPTY_MOVE'
        elif status ==3:
            st_status = 'LOADING'
        elif status ==4:
            st_status = 'LOADED_MOVE'
        elif status ==5:
            st_status = 'LOADED_STOP'
        elif status ==6:
            st_status = 'DUMPING'
        time_stamp=round((time_stamp/1000.),2)
        time_diff=round(((time_stamp-time_old)),2)
        ton = (ton/1000)
        filter = (filter/1000)
        speed = (speed/1000)
        slopecal(ton)#get the slope curve
        tonfilter(ton,speed)#get the right tonnage and status
        print("time_stamp (seg): ", time_stamp," time_diff: ",time_diff," tons: ", ton," ton filtered: ", filter," speed: ",speed ," status: ", st_status," filter ton: ", _ton," new status: ", _status, " slope: ", _slope )
        _time.append(time_stamp)
        _raw_ton.append(ton)
        _filt_ton.append(_ton)
        _filt_status.append(_status)
        with open('/Users/jav/Desktop/komatsu.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["time_stamp (seg): ", time_stamp," time_diff: ",time_diff," tons: ", ton," ton filtered: ", filter," speed: ", speed," status: ", st_status, " Filter ton: ",_ton, " new Status: ", _status, " slope: ", _slope])
        time_old = time_stamp
        #drawnow(makeFig)
        #break
    drawnow(makeFig)
    plt.pause(30)


def tonfilter(ton,_speed):
    """
    Filters status and payload to a new _status and _ton
    :param raw ton, speed:
    :return:
    """
    global  _ton
    global _status
    global _status_old
    min_ton = 13

    if ton <= min_ton and _speed >= 5 :
      _ton = 0
      _status = 'EMPTY_TRAVEL'
    elif ton <= min_ton and _speed < 5  :
        _ton = 0
        _status = 'EMPTY_STOP'
    elif ton > min_ton  and _speed < 5 and _slope == 1 and (_status_old == 'EMPTY_STOP' or _status_old == 'LOADING'):
        _ton = ton
        _status = 'LOADING'
    elif ton >= 140 and _speed > 5 :
        _ton = ton
        _status = 'LOADED_MOVE'
    elif ton >= 140 and _speed <= 5 and _slope == 1 :
        _ton = ton
        _status = 'LOADED_STOP'
    elif ton > min_ton and ton <= 135 and _speed < 5 and _slope == -1 and (_status_old == 'LOADED_STOP' or _status_old == 'LOADED_MOVE' or _status_old == 'DUMPING'):
        _ton = ton
        _status = 'DUMPING'
    else :
        _ton = ton
    _status_old = _status

def slopecal(ton):
    """
    Calculates the Slope of the variables
    :param raw ton:
    :return:
    """
    global _ton_old
    global _slope

    print("ton: ", ton, " _ton_old: ", _ton_old, " substraction: ", round((ton - _ton_old),2))

    if  round((ton - _ton_old), 2) >= 5:
        _slope = 1
    if round((ton - _ton_old), 2) <= -10:
        _slope = -1
    _ton_old = ton

def makeFig():
    global _time,_raw_ton,_filt_ton
    #plt.rcParams.update({'font.size': 5})
    plt.subplot(121)
    plt.plot(_time, _raw_ton, label='linear')
    plt.xticks(fontsize=5)
    plt.title('1')

    plt.subplot(122)
    plt.plot(_time, _filt_ton, label='linear')
    plt.xticks(fontsize=5)
    plt.title('2')

    #plt.xlabel('Date:time')
    #plt.ylabel('Temp')









def main():
    print("##################################################################################################")
    database = path_to_DB
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        payload_status(conn)
 
 
if __name__ == '__main__':
    main()