#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from click import echo, style, clear
from mysql.connector import Error
from .track import track_exists

def add(db, cursor, number, tname, track, year):

    '''
    Add a new subject (module)
    '''

    res = track_exists(db, cursor, tname, track, year)
    if res == 0:
        echo(style(' [x] ', fg='red', bold=True) + style('{} {} doesn\'t exist in tracks table.'.format(track, year), bold=True))
        return 1

    for subject in range(1, number+1):
        echo(style(' [!] ', fg='blue', bold=True) + style('Subject {} / {}: '.format(subject, number), bold=True))

        query = 'INSERT INTO `{}_{}_Subjects` (code, name, teacher, start_week, end_week, start_hour, end_hour, day) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'.format(track, year)

        valid_code = False
        while(not valid_code):
            code = str(input(style(' [?] ', fg='yellow', bold=True) + style('Subjects code: ', bold=True)))
            valid_code = validate_code(code)
            if not valid_code : echo(style(' [x] ', fg='red', bold=True) + style('Invalid date format [Mx where x is one or more number].', bold=True))

        name = str(input(style(' [?] ', fg='yellow', bold=True) + style('Subject Name: ', bold=True)))

        teacher = str(input(style(' [?] ', fg='yellow', bold=True) + style('Teacher of the Subject: ', bold=True)))
        start_week = int(input(style(' [?] ', fg='yellow', bold=True) + style('Start Week: ', bold=True)))
        end_week = int(input(style(' [?] ', fg='yellow', bold=True) + style('End Week: ', bold=True)))

        valid_hour = False
        while(not valid_hour):
            start_hour = str(input(style(' [?] ', fg='yellow', bold=True) + style('Start time: ', bold=True)))
            end_hour = str(input(style(' [?] ', fg='yellow', bold=True) + style('End time: ', bold=True)))
            valid_hour = validate_hour(start_hour) and validate_hour(end_hour)
            if not valid_hour : echo(style(' [x] ', fg='red', bold=True) + style('Invalid hour format [hh:mm] 24-hour.', bold=True))

        valid_day = False
        while(not valid_day):
            day = str(input(style(' [?] ', fg='yellow', bold=True) + style('Day: ', bold=True)))
            valid_day = validate_day(day)
            if not valid_day : echo(style(' [x] ', fg='red', bold=True) + style('Invalid day format [MON-SUN].', bold=True))

        try:
            cursor.execute(query, (code, name, teacher, start_week, end_week, start_hour, end_hour, day))
            db.commit()
            echo(style(' [\u2713] ', fg='green', bold=True) + style('{} added successfully in `{}_{}_Subjects`.'.format(name.strip(), track, year), bold=True))
        except Error as err:
            echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

    cursor.close()
    db.close()

def delete(db, cursor, track, year, code):
    '''
    Delete a subject (module)
    '''

    query = "DELETE FROM `{}_{}_Subjects` WHERE code=\'{}\'".format(track, year, code)

    try:
        cursor.execute(query)
        db.commit()
        echo(style(' [\u2713] ', fg='green', bold=True) + style('{} subject deleted successfully in `{}_{}_Subjects`.'.format(code, track, year), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def list(db, cursor, track, year):

    '''
    Print out all subjects (Modules) available.
    '''

    query = "SELECT * FROM {}_{}_Subjects".format(track, year)

    try:
        cursor.execute(query)
        subjects = cursor.fetchall()

        for subject in subjects:
            echo(style(' [->] ', fg='cyan', bold=True) + style('{}: {} ({})'.format(subject['code'], subject['name'], subject['teacher']), bold=True))
            echo(style('    [->] ', fg='yellow', bold=True) + style('Weeks: {} -> {}'.format(subject['start_week'], subject['end_week']), bold=True))
            echo(style('    [->] ', fg='yellow', bold=True) + style('Time: {} from {} to {}'.format(subject['day'], subject['start_hour'], subject['end_hour']), bold=True))

    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def validate_code(code):
    regex_code = "M[0-9]+"
    validate = re.match(regex_code, code)
    return validate

def validate_hour(hour):
    regex_hour = "^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$"
    validate = re.match(regex_hour, hour)
    return validate

def validate_day(day):
    regex_day = "\\b((MON|TUE|WED|THU|FRI|SAT|SUN))\\b"
    validate = re.match(regex_day, day)
    return validate
