#!/usr/lib/python3

# ---------------------------------------------- Instructions ----------------------------------------- #
"""
The sensor is connected using USB comminication through a TTL to USB converter. The wiring is at follows:

    RED-ORANGE  (Vin)    -> 3.3v (NOT 5v !!!!!!!!) - RPi Pin 2  -
    BLACK-BROWN (GND)    -> GND                    - RPi Pin 14 -
    YELLOW-BLUE (TxD)    -> WHITE in TTL (TxD)
    WHITE-GREEN (RxD)    -> GREEN in TTL (RxD)

Linux Kernel creates a corresponding file to use name 'ttyUSB0', this is our port of communication.
Speed (Baud Rate) of the port must be 9600*N where N is between 1 and 12. 6 is the default value.
The module has an identifying changeable address used to communicate data between the module and Raspberry Pi. (0xFFFFFFFF by default)
Accessing the module is assured by a changeable password. (0x00000000 by default)

For a fingerprint to be stored, it passes by these steps (not necessarily all of them):

    1. Detect the finger and take its image.
    2. Store the image of the fingerprint in the image buffer.
    3. Convert the image buffer data to characterics and stores them in the first char buffer.
    4. Check if the template already exists.
    5. If not, Take another image of the same finger.
    6. Store it in the image buffer.
    7. Convert it to characterics and stores them in the second char buffer.
    8. Compare both buffer.
    9. If they match, template is created and stored.

"""
# ---------------------------------------------------------------------------------------------------- #

# --------------------- Libraries -------------------- #
import time
import json
from os import path
from pyfingerprint.pyfingerprint import PyFingerprint
import lcd_i2c_driver
# ---------------------------------------------------- #

# --------------------- Functions -------------------------- #

# Function that add the student into the JSON file.
def addStudent(id, fname, lname, cin, cne):
    # if the file does not exist
    if(path.exists('GSEII2.json')==False):
        # create it and write the initial data in it
        with open('GSEII2.json', 'w+') as file:
            data = {}
            data['students'] = []
            json.dump(data, file)
        file.close()

    # load existing json data
    with open('GSEII2.json', 'r') as file:
        data = json.load(file)
    file.close()

    # append the new student
    student = {'id': id,
               'first_name': fname,
               'last_name': lname,
               'cin': cin,
               'cne': cne}
    data['students'].append(student)

    # write the new json data into the file
    with open('GSEII2.json', 'w') as file:
        json.dump(data, file)
    file.close()
# LCD write simplified
def lcd_write(firstline, secondline=''):
    lcd.lcd_clear()
    lcd.lcd_display_string(firstline, 1)
    lcd.lcd_display_string(secondline, 2)
# ----------------------------------------------------------- #

# -------------------------------------- Initializing --------------------------------------- #
try:
    # making sure that the JSON file exists
    if(path.exists('GSEII2.json')==False): raise Exception('File of students doesn\'t exist.')
    # connecting to the sensor
    f = PyFingerprint(port='/dev/ttyUSB0',
                      baudRate=9600*6,
                      address=0xFFFFFFFF,
                      password=0x00000000)
    # verify password
    if(f.verifyPassword()==False): raise Exception('Sensor\'s password is incorrect.')
    # Initializing the LCD
    lcd = lcd_i2c_driver.lcd()
except KeyboardInterrupt:
    exit(1)
except Exception as e:
    print('Error: ' + str(e))
    exit(1)
# ------------------------------------------------------------------------------------------- #

# --------------------------------------- Main Program -------------------------------------- #
print("Enrolling fingerprints...")
try:
    while(1):
        time.sleep(2) # for stabilizing the sensor
        ''' First Read '''
        # wait for finger to be detected
        lcd_write('Waiting for', 'finger...')
        while(f.readImage()==False): pass
        # convert its image to the first char buffer (0x01)
        f.convertImage(0x01)
        # search if the template already exits
        result = f.searchTemplate()
        # get the position number of found template
        positionNumber = result[0]
        # if the value is positive
        if (positionNumber >= 0):
            lcd_write('Template exits', 'at #' + str(positionNumber))
            continue

        lcd_write('Remove finger')
        time.sleep(2)

        ''' Second Read '''
        # wait for finger to be detected
        lcd.lcd_clear()
        lcd_write('Waiting for', 'same finger...')
        while (f.readImage()==False): pass
        # convert its image to the first char buffer (0x02)
        f.convertImage(0x02)
        # compares char buffers
        if (f.compareCharacteristics()==0):
            lcd_write('Fingers do', 'not match')
            continue
        # creates a template: combine the characterics of the two char buffers
        # and add student to JSON file.
        if(f.createTemplate()==True):
            # get student info
            lcd_write('Please enter', 'your info')
            fname = input('Please enter first name:\n')
            lname = input('Please enter last name:\n')
            cin = input('Please enter CIN:\n')
            cne = input('Please enter CNE:\n')
            # store the template in the next available position
            positionNumber = f.storeTemplate()
            lcd_write(fname +" "+ lname, 'enrolled')
            # add it to Json file
            addStudent(positionNumber, fname, lname, cin, cne)
        else:
            lcd_write('Error adding', 'template')
except KeyboardInterrupt:
    print()
    exit()
except Exception as e:
    lcd.lcd_clear()
    print('Error: ' + str(e))
    exit(1)
