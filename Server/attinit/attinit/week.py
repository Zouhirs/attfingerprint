#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from click import echo, style, clear
from mysql.connector import Error
from datetime import datetime, timedelta
import re

def create(db, cursor, name):

    '''
    Create table that contains Weeks (Liste des semaines).
    '''

    query = '''CREATE TABLE `{}`(
        `number` int(2) NOT NULL AUTO_INCREMENT,
        `start_date` varchar(10) NOT NULL,
        `end_date` varchar(10) NOT NULL,
        PRIMARY KEY(`number`)
    ) ENGINE=InnoDB '''.format(name)

    try:
        cursor.execute(query)
        echo(style(' [\u2713] ', fg='green', bold=True) + style('Table `{}` created.'.format(name), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def drop(db, cursor, name):

    '''
    Delete weeks (liste des semaines) table.
    '''

    query = "DROP TABLE `{}`".format(name)

    try:
        cursor.execute(query)
        db.commit()
        echo(style(' [\u2713] ', fg='green', bold=True) + style('Table `{}` deleted.'.format(name), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def add(db, cursor, name, start_date, end_date):

    '''
    Add a week info manually.
    '''

    query = "INSERT INTO `{}` (`start_date`, `end_date`) VALUES (%s, %s)".format(name)

    if not validate_date(start_date) or not validate_date(end_date):
        echo(style(' [x] ', fg='red', bold=True) + style('Date format is invalid. Need to be [yyyy-mm-dd].', bold=True))
        return 1
    try:
        cursor.execute(query ,(start_date, end_date))
        db.commit()
        echo(style(' [\u2713] ', fg='green', bold=True) + style('{} -> {}.'.format(start_date , end_date), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def addauto(db, cursor, name, start, total, week_manual, _days_study):

    '''
    Automatically insert weeks with the option of choosing weeks to enter manually.
    '''

    for week in range(1, int(total)+1):

        if str(week) in week_manual:
            valide = False

            while(not valide):
                start = str(input(style(' [?] ', fg='yellow', bold=True) + style('Start date of week {} [yyyy-mm-dd]: '.format(week), bold=True)))
                valide = validate_date(start)
                if not valide : echo(style(' [x] ', fg='red', bold=True) + style('Invalid date format.', bold=True))

            start_date, end_date, next_date = calculate_date(start, _days_study)

        else:
            start_date, end_date, next_date = calculate_date(start, _days_study)

        query = "INSERT INTO `{}` (start_date, end_date) VALUES (%s, %s)".format(name)

        try:
            cursor.execute(query ,(start_date, end_date))
            db.commit()
            echo(style(' [\u2713] ', fg='green', bold=True) + style('{} -> {} added successfully in `{}`.'.format(start_date, end_date , name), bold=True))
        except Error as err:
            echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
            return 1

        start = str(next_date)

def list(db, cursor, name):

    '''
    List weeks (liste des semaines).
    '''

    query = "SELECT * FROM {}".format(name)

    try:
        cursor.execute(query)
        weeks = cursor.fetchall()

        for week in weeks:
            echo(style(' [->] ', fg='cyan', bold=True) + style('{}: {} -> {}'.format(week['number'], week['start_date'], week['end_date']), bold=True))

    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def modify(db, cursor, name, number):

    '''
    Modify the start date and/or end date of a week.
    '''

    new_start_date = str(input(style(' [?] ', fg='yellow', bold=True) + style('New start date: ', bold=True)))
    new_end_date = int(input(style(' [?] ', fg='yellow', bold=True) + style('New end date: ', bold=True)))
    if not validate_date(start_date) or not validate_date(end_date):
        echo(style(' [x] ', fg='red', bold=True) + style('Date format is invalid. Need to be [yyyy-mm-dd].', bold=True))
        return 1

    query = "UPDATE {} SET `start_date`=\'{}\', `end_date`={} WHERE `number`={}".format(name, new_start_date, new_end_date, number)

    try:
        cursor.execute(query)
        db.commit()
        echo(style(' [\u2713] ', fg='green', bold=True) + style('Week {} modified successfully to {} -> {}.'.format(number, new_start_date , new_end_date), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def calculate_date(start_date, _days_study):

    '''
    Calculate date of start, end and next start.
    '''

    year, month, day = map(int, start_date.split('-'))

    start_datetime = datetime(year, month, day)
    end_datetime = start_datetime + timedelta(days=_days_study-1)
    next_datetime = end_datetime + timedelta(days=8-_days_study)

    start = start_datetime.strftime('%Y-%m-%d')
    end = end_datetime.strftime('%Y-%m-%d')
    next = next_datetime.strftime('%Y-%m-%d')

    return start, end, next

def validate_date(date):

    '''
    Validate date format provided by the user with regex.
    '''

    regex_date = "^([0-2][0-9]|(3)[0-1])(-)(((0)[0-9])|((1)[0-2]))(-)\d{4}$"
    validate = re.match(regex_date, date)
    return validate
