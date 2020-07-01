#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import time
import threading
from datetime import date, datetime
import RPi.GPIO as GPIO
from mysql.connector import Error
from pyfingerprint.pyfingerprint import PyFingerprint
import lcd_i2c_driver
from click import echo, style, clear

gpio_RED = 24
gpio_GREEN = 23
gpio_BUZZER = 22

PERIOD_RUNNING = 60*30 # timeout period


@click.command()
@click.option('-s', '--server', '_server', type=str, default='127.0.0.1', nargs=1, help='Server IPv4 address. (Default: 127.0.0.1)')
@click.option('-u', '--user', '_user', type=str, required=True, nargs=1, help='Username.')
@click.option('-p', '--password', '_password', required=True, nargs=1, help='Password.')
@click.option('-b', '--database', '_database', type=str, required=True, nargs=1, help='Database name.')
@click.option('-t', '--track', '_track', type=str, required=True, nargs=1, help='Academic track.')
@click.option('-y', '--year', '_year', type=int, required=True, nargs=1, help='Academic year of track.')
@click.option('-w', '--weeks', '_weeks', type=str, default='Weeks', nargs=1, help='Name of table of weeks (Default: Weeks)')
@click.option('-d', '--device', '_device', type=click.Path(exists=True), required=True, nargs=1, help='Sensor\'s file in /dev. (/dev/ttyUSB*)')
def main(_server, _user, _password, _database, _track, _year, _weeks, _device):
	try:

		from .connect import connect
		db, cursor = connect(_server, _user, _password, _database)

		_fsensor, lcd = init(_device)

		if db is not None and cursor is not None and _fsensor is not None and lcd is not None:

			init(_device)

			start = time.time() # get current time

			present_students = []

			current_week = getCurrentWeek(db, cursor, _weeks)
			# current_subject = getCurrentSubject(db, cursor, _track, _year, _weeks)
			current_subject = 'M251'
			if current_week is None or current_subject is None: return

			while True:
				lcd_write(lcd, 'Waiting for', 'finger. S{}|{}'.format(current_week, current_subject))
				id = read_fingerprint(_fsensor, timeout=start + PERIOD_RUNNING)
				if id is None: return
				elif id == -1:
					threading.Thread(target=beep, args=(1,0.2)).start()
					leds(2)
					lcd_write(lcd, 'No match', 'Please try again')
				else:
					threading.Thread(target=beep, args=(2,0.05)).start()
					leds(1)
					student = getStudentFromID(db, cursor, _track, _year, id)[0]
					if not student :
						lcd_write(lcd, 'Sensor & server', 'are not in sync!')
					else:
						if student['id'] in present_students:
							lcd_write(lcd, 'Already', 'Registred')
						else:
							status = getStatus(db, cursor, _track, _year, current_week, current_subject, id)
							setToPresent(db, cursor, _track, _year, current_week, current_subject, id, status)
							lcd_write(lcd, student['first_name'], student['last_name'])
							present_students.append(student['id'])

				time.sleep(3)

	except Exception as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

	cursor.close()
	db.close()
	GPIO.output(gpio_RED, GPIO.LOW)
	GPIO.output(gpio_GREEN, GPIO.LOW)
	GPIO.output(gpio_BUZZER, GPIO.LOW)
	GPIO.cleanup()
	lcd.lcd_clear()


def beep(count, period):
	for i in range(count):
		GPIO.output(gpio_BUZZER, GPIO.HIGH)
		time.sleep(period)
		GPIO.output(gpio_BUZZER, GPIO.LOW)
		time.sleep(period)

def leds(mode):
	if(mode==0): # waiting
		GPIO.output(gpio_GREEN, GPIO.HIGH)
		GPIO.output(gpio_RED, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(gpio_RED, GPIO.LOW)
		GPIO.output(gpio_GREEN, GPIO.LOW)
	elif(mode==1): # template found
		GPIO.output(gpio_GREEN, GPIO.HIGH)
		GPIO.output(gpio_RED, GPIO.LOW)
	elif(mode==2): # template not found
		GPIO.output(gpio_GREEN, GPIO.LOW)
		GPIO.output(gpio_RED, GPIO.HIGH)
	else: raise ValueError("Leds mode not supported.")

def lcd_write(lcd, firstline, secondline=''):
	lcd.lcd_clear()
	lcd.lcd_display_string(firstline, 1)
	lcd.lcd_display_string(secondline, 2)

def init(device):

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(gpio_RED, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(gpio_GREEN, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(gpio_BUZZER, GPIO.OUT, initial=GPIO.LOW)

	baudrate = 57600
	address = 0xFFFFFFFF
	password = 0x00000000
	fsensor = PyFingerprint(device, baudrate, address, password)

	if not fsensor.verifyPassword(): raise Exception('Sensor\'s password is incorrect.')
	lcd = lcd_i2c_driver.lcd()

	beep(2,0.05)
	return fsensor, lcd

def read_fingerprint(sensor, timeout=30):
	while(sensor.readImage()==False):
		leds(0)
		if (time.time() > timeout) : return None
	sensor.convertImage(0x01)
	result = sensor.searchTemplate()
	return result[0]

def getCurrentWeek(db, cursor, weeks):
	day = date.today().strftime("%Y-%m-%d")

	query = "SELECT `number` FROM `{}` WHERE '{d}' <= `end_date` and '{d}' >= `start_date`".format(weeks, d=day)

	try:
		cursor.execute(query)
		current_week = cursor.fetchall()
	except Error as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
		return None

	if current_week: return current_week[0]['number']
	else: return None

def getCurrentSubject(db, cursor, track, year, weeks):
	now = datetime.now()
	day = now.strftime("%a")
	hour = now.strftime("%H:%M")

	current_week = getCurrentWeek(db, cursor, weeks)

	if current_week is None: return None

	query = '''SELECT `code`, `name` FROM `{}_{}_Subjects`
			   WHERE {} BETWEEN start_week AND end_week
			   AND day='{}' AND '{h}' >=start_hour AND '{h}' < end_hour'''.format(track, year, current_week, day, h=hour)

	try:
		cursor.execute(query)
		current_subject = cursor.fetchall()
	except Error as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
		return None

	if current_subject: return current_subject[0]['code']
	else: return None

def getStudentFromID(db, cursor, track, year, id):
	query = "SELECT * FROM `{}_{}_Students` WHERE id={}".format(track, year, id)

	try:
		cursor.execute(query)
		student = cursor.fetchall()
		return student
	except Error as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
		return None

def getStatus(db, cursor, track, year, current_week, current_module, id):

	query = "SELECT `S{}` FROM `{}_{}_{}` WHERE `id`={}".format(current_week, track, year, current_module, id)

	try:
		cursor.execute(query)
		status = cursor.fetchall()
	except Error as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
		return None

	if status: return status[0]['S{}'.format(current_week)]
	else: return None

def setToPresent(db, cursor, track, year, current_week, current_module, id, status):
	value = '1P'
	if status == '1P': value = '2P'

	query = "UPDATE `{}_{}_{}` SET `S{}`='{}' WHERE id={}".format(track, year, current_module, current_week, value, id)

	try:
		cursor.execute(query)
		db.commit()
	except Error as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
		return None
