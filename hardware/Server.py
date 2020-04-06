#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This code will be used to acces our database in the server
'''

# --------------------- Libraries -------------------- #
import mysql.connector as mysql
from datetime import date, datetime
import Info
# ---------------------------------------------------- #

# for simulation purposes

# days = {'15':"MON", # 12:00 to 12:59 -> Monday
#         '16':"TUE", # 13:00 to 13:59 -> Tuesday
#         '17':"WED", # ...
#         '18':"THU",
#         '19':"FRI",
#         '20':'SAT'}

# 00min -> 8h30 | 12min -> 10h30 | 36min -> 14h30 | 48min -> 16h30
#------------------------------------------------------ Functions ----------------------------------------------------------- #

'''
Connect to database in server.
'''
def connect():
    global mydb
    global mycursor
    mydb = mysql.connect(host=Info.host, user=Info.mysql_user, password=Info.mysql_password, database=Info.database_name)
    mycursor = mydb.cursor()

'''
Retrieve the current study week.
'''
def getCurrentWeek():
    day = date.today().strftime("%Y-%m-%d")
    #mycursor.execute("SELECT `number` FROM `weeks` WHERE days='" + day + "'")
    mycursor.execute("SELECT `number` FROM `weeks` WHERE '" + day + "' <= `last_day` and '" + day + "' >= `first_day`")
    myresult = mycursor.fetchall()
    if(len(myresult)!=0): return myresult[0][0]
    else: return None

'''
Retrive the current module based on current time.
'''
def getCurrentModule():
    now = datetime.now()
    # day = now.strftime("%H")
    # hour = now.strftime("%M")
    day = now.strftime("%a")
    hour = now.strftime("%H:%M")
    s = getCurrentWeek()
    if s is None: return None
    #mycursor.execute("SELECT `id`, `name` FROM `subjects` WHERE "+str(s)+" BETWEEN first_week AND last_week AND day='"+days[day]+"' AND "+hour+ ">=start_time AND "+hour+"<= end_time")
    mycursor.execute("SELECT `id`, `name` FROM `subjects` WHERE "+str(s)+" BETWEEN first_week AND last_week AND day='"+day+"' AND '"+hour+ "' >=start_time AND '"+hour+"' <= end_time")
    myresult = mycursor.fetchall()
    if(len(myresult)!=0): return myresult[0][0], myresult[0][1]
    else: return None

'''
Get current student stat based on id, if he's present or not.
'''
def getStatus(id):
    mycursor.execute("SELECT `S"+str(getCurrentWeek())+"` FROM `" + getCurrentModule()[0] + "` WHERE `id`="+str(id))
    myresult = mycursor.fetchall()
    return myresult[0][0]

'''
Set the student to present, 1P for present 2-hours, 2P for present 4-hours.
'''
def setToPresent(id):
    value = '1P'
    if getStatus(id) == '1P': value = '2P'
    mycursor.execute("UPDATE `"+getCurrentModule()[0]+"` SET `S"+str(getCurrentWeek())+"`='"+str(value)+"' WHERE id="+str(id)+"")
    mydb.commit()

'''
Close connection.
'''
def close():
    mycursor.close()
    mydb.close()
# ------------------------------------------------------------------------------------------------------------------------ #

if __name__ == "__main__":
    connect()
    print("Current Week: " + str(getCurrentWeek()))
    print("Current Module: " + str(getCurrentModule()))
    close()
