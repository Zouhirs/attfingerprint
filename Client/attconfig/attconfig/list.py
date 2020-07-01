#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql.connector import Error
from click import echo, style, clear

def list(db, cursor, sensor, track, year):
    '''
    List All Students and Sensor's Status:
    - Load students data from database.
    - Print every student.
    - Print sensor's memory status.
    '''

    clear()

    query = "SELECT * FROM {}_{}_Students".format(track, year)

    try:
        cursor.execute(query)
        students = cursor.fetchall()
        for student in students:
            echo(style('[{}] - '.format(student['id']), fg='yellow', bold=True) + style('{} {}'.format(student['first_name'], student['last_name']), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

    used = sensor.getTemplateCount()
    total = sensor.getStorageCapacity()
    echo(style('\nUsed templates: \n', bold=True) + style('{} / '.format(used), fg='blue', bold=True) + style('{}.'.format(total)))
