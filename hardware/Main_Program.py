#!/usr/lib/env python

# --------------------- Libraries -------------------- #
import json
import time
import threading
import Module as m
import Info
import Server
# ---------------------------------------------------- #

# -------------------------------------- Initializing --------------------------------------- #
try:
    m.init()
except FileNotFoundError as fnfe:
    print('File of students doesn\'t exist.')
    exit(1)
except Exception as e:
    print("Initializing Error " + str(e))
    exit(1)
# ------------------------------------------------------------------------------------------- #

# --------------------------------------- Main Program -------------------------------------- #
try:
    start = time.time() # get current time
    PERIOD_OF_TIME = 60*2 # timeout period
    timeout = False
    presentStudentsIds = []
    with open(Info.studentFilePath, 'r') as file: # load students file
        data = json.load(file)
        file.close()
    while(1):
        m.lcd_write('Waiting for', 'finger | ' + str(Server.getCurrentModule()))
        while(m.fingerSensor.readImage()==False): # waiting for finger
            m.leds(0)
            if (time.time() > start + PERIOD_OF_TIME) : # check timeout
                timeout = True
                break
        if timeout == True: break # check timeout
        m.lcd_write('Searching...')
        pos = m.searchFingerprint()
        if (pos is None):
            beep_sound = threading.Thread(target=m.beep, args=(1,0.2))
            beep_sound.start()
            m.leds(2)
            m.lcd_write('No match', 'Please try again')
        else:
            beep_sound = threading.Thread(target=m.beep, args=(2,0.05))
            beep_sound.start()
            m.leds(1)
            student = m.getStudentFromID(pos, data)
            if student['id'] not in presentStudentsIds:
                m.lcd_write(student['first_name'], student['last_name'])
                Server.setToPresent(str(student['id']))
                presentStudentsIds.append(student['id'])
            else:
                m.lcd_write('Already', 'Registred')
        time.sleep(2)
    m.cleanup()
except KeyboardInterrupt as ke:
    m.cleanup()
    print()
    exit()
except Exception as e:
    m.cleanup()
    print("Program error: " + str(e))
    exit(1)
