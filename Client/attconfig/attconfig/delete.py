#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from click import echo, style, clear
from mysql.connector import Error
from .list import list

def delete(db, cursor, sensor, track, year):
    '''
    Delete a Student From Sensor and File:
    - Get id of student to delete.
    - Load data from server.
    - Remove student from server and sensor.
    '''

    clear()

    list(db, cursor, sensor, track, year)
    id = int(input(style(' [?] ', fg='yellow', bold=True) + style('ID of student to delete: ', bold=True)))

    query = "DELETE FROM {}_{}_Students WHERE `id`={}".format(track, year, id)

    try:
        cursor.execute(query)
        db.commit()
        res = sensor.deleteTemplate(id)
        if res : echo(style(' [\u2713] ', fg='green', bold=True) + style('Student with ID {} has been removed.\n'.format(id), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def delete_all(db, cursor, sensor, track, year):
    '''
    Delete All Students:
    - Load data from file.
    - Empty data.
    - Insert raw data in file.
    - Delete all templates in sensor.
    '''

    list(db, cursor, sensor, track, year)

    query = "DELETE FROM {}_{}_Students".format(track, year, id)

    try:
        cursor.execute(query)
        db.commit()
        res = sensor.clearDatabase()
        if res : echo(style(' [\u2713] ', fg='green', bold=True) + style('All students have been removed.\n', bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
