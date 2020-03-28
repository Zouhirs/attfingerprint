'''
This code will be used to acces our database in the server
'''

# --------------------- Libraries -------------------- #
import mysql.connector as mysql
from datetime import date, datetime
import Info
# ---------------------------------------------------- #

# for simulation purposes

days = {'23':"MON", # 12:00 to 12:59 -> Monday
        '00':"TUE", # 13:00 to 13:59 -> Tuesday
        '01':"WED", # ...
        '02':"THU",
        '03':"FRI",
        '04':'SAT'}

# 00min -> 8h30 | 12min -> 10h30 | 36min -> 14h30 | 48min -> 16h30

#------------------------------------------------------ Functions ----------------------------------------------------------- #
def connect():
    global mydb
    global mycursor
    mydb = mysql.connect(host=Info.host, user=Info.mysql_user, password=Info.mysql_password, database=Info.database_name)
    mycursor = mydb.cursor()

def getCurrentWeek():
    day = date.today().strftime("%Y-%m-%d")
    mycursor.execute("SELECT `number` FROM `weeks` WHERE days='" + day + "'")
    myresult = mycursor.fetchall()
    if myresult is not None: return myresult[0][0]
    else: return None

def getCurrentModule():
    now = datetime.now()
    day = now.strftime("%H")
    hour = now.strftime("%M")
    s = getCurrentWeek()
    mycursor.execute("SELECT `id` FROM `subjects` WHERE "+str(s)+" BETWEEN first_week AND last_week AND day='"+days[day]+"' AND "+hour+ ">=start_time AND "+hour+"<= end_time")
    myresult = mycursor.fetchall()
    if(len(myresult)!=0): return myresult[0][0]
    else: return None

def getStatus(id):
    mycursor.execute("SELECT `S"+str(getCurrentWeek())+"` FROM `" + getCurrentModule() + "` WHERE `id`="+str(id))
    myresult = mycursor.fetchall()
    return myresult[0][0]

def setToPresent(id):
    value = '1P'
    if getStatus(id) == '1P': value = '2P'
    mycursor.execute("UPDATE `"+str(getCurrentModule())+"` SET `S"+str(getCurrentWeek())+"`='"+str(value)+"' WHERE id="+str(id)+"")
    mydb.commit()

def close():
    mycursor.close()
    mydb.close()
# ------------------------------------------------------------------------------------------------------------------------ #
