#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from click import echo, style, clear
from mysql.connector import Error

def create(db, cursor, name):

    '''
    Create table that contains Tracks (Filieres).
    '''

    query = '''CREATE TABLE `{}`(
        `id` varchar(10) NOT NULL,
        `year` int(1) NOT NULL,
        PRIMARY KEY(`id`, `year`)
    ) ENGINE=InnoDB '''.format(name)

    try:
        cursor.execute(query)
        echo(style(' [\u2713] ', fg='green', bold=True) + style('Table `{}` created.'.format(name), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def drop(db, cursor, name):

    '''
    Delete tracks (filieres) table and all related tables for every track (filiere).
    '''

    query = "SELECT * FROM {}".format(name)

    try:
        cursor.execute(query)
        tracks = cursor.fetchall()

        for track in tracks:
            delete(db, cursor, name, track['name'], track['year'])
    except Exception as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def add(db, cursor, name, track, year):

    '''
    Add a track (filiere) to the table and create correspondant tables.
    '''
    if track_exists(db, cursor, name, track, year):
        echo(style(' [x] ', fg='red', bold=True) + style('{} {} already exists.'.format(track, year), bold=True))
        return
    query1 = "INSERT INTO `{}` (`id`, `year`) VALUES (%s, %s)".format(name)
    subquery2 = '''CREATE TABLE `{}_{}_Students` (
        `id` int(4) NOT NULL,
        `first_name` varchar(20) NOT NULL,
        `last_name` varchar(40) NOT NULL,
        PRIMARY KEY(`id`),
        INDEX(`first_name`),
        INDEX(`last_name`)
    ) ENGINE=InnoDB'''.format(track, year)
    subquery3 = '''CREATE TABLE `{}_{}_Subjects` (
        `code` varchar(4) NOT NULL,
        `name` varchar(50) NOT NULL,
        `teacher` varchar(20) NOT NULL,
        `start_week` INT(2) NOT NULL,
        `end_week` INT(2) NOT NULL,
        `start_hour` varchar(5) NOT NULL,
        `end_hour` varchar(5) NOT NULL,
        `day` VARCHAR(3) NOT NULL,
        PRIMARY KEY(`code`)
    ) ENGINE=InnoDB'''.format(track, year)
    subquery4 = '''CREATE TABLE `{}_{}_Teachers` (
        `id` int(4) NOT NULL,
        `first_name` varchar(20) NOT NULL,
        `last_name` varchar(40) NOT NULL,
        PRIMARY KEY(`id`)
    ) ENGINE=InnoDB'''.format(track, year)

    try:
        cursor.execute(query1 ,(track, year))
        cursor.execute(subquery2)
        cursor.execute(subquery3)
        cursor.execute(subquery4)
        db.commit()
        echo(style(' [\u2713] ', fg='green', bold=True) + style('{} {} added successfully in `{}`.'.format(track, year , name), bold=True))
        echo(style(' [\u2713] ', fg='green', bold=True) + style('{}_{}_Students created successfully`.'.format(track, year), bold=True))
        echo(style(' [\u2713] ', fg='green', bold=True) + style('{}_{}_Subjects created successfully.'.format(track, year), bold=True))
        echo(style(' [\u2713] ', fg='green', bold=True) + style('{}_{}_Teachers created successfully.'.format(track, year), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def list(db, cursor, name):

    '''
    Print out all tracks (filieres) available.
    '''

    query = "SELECT * FROM {}".format(name)

    try:
        cursor.execute(query)
        tracks = cursor.fetchall()

        for track in tracks:
            echo(style(' [->] ', fg='cyan', bold=True) + style('{} {}'.format(track['id'], track['year']), bold=True))

    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def delete(db, cursor, name, track, year):

    '''
    Delete a track (filiere) and all correspondant tables.
    '''
    if not track_exists(db, cursor, name, track, year):
        echo(style(' [x] ', fg='red', bold=True) + style('{} {} does not exist.'.format(track, year), bold=True))
        return

    query1 = "DELETE FROM `{}` WHERE id=\'{}\' AND year={}".format(name, track, year)
    query2 = "SELECT table_name FROM information_schema.tables WHERE table_name REGEXP \'^.*({}_{}).*$\'".format(track, year)

    try:
        cursor.execute(query1)
        db.commit()

        cursor.execute(query2)
        tables = cursor.fetchall()

        for table in tables:
            subquery = "DROP TABLE {}".format(table['table_name'])
            cursor.execute(subquery)
            db.commit()

        echo(style(' [\u2713] ', fg='green', bold=True) + style('{} {} deleted successfully from `{}` with all its related tables.'.format(track, year , name), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def rename(db, cursor, name, track, year):

    '''
    Rename a track (filiere) and all its correspondant tables name.
    '''
    if not track_exists(db, cursor, name, track, year):
        echo(style(' [x] ', fg='red', bold=True) + style('{} {} does not exist.'.format(track, year), bold=True))
        return

    new_track = str(input(style(' [?] ', fg='yellow', bold=True) + style('New track name: ', bold=True)))
    new_year = int(input(style(' [?] ', fg='yellow', bold=True) + style('New track year: ', bold=True)))
    if new_track == "": new_track = track
    if new_year == "": new_year = year

    query1 = "UPDATE {} SET `id`=\'{}\', `year`={} WHERE `id`=\'{}\'".format(name, new_track, new_year, track)
    query2 = "SELECT table_name FROM information_schema.tables WHERE table_name REGEXP \'^.*({}_{}).*$\'".format(track, year)


    try:
        cursor.execute(query1)
        db.commit()

        cursor.execute(query2)
        tables = cursor.fetchall()

        for table in tables:
            mtrack, myear, msubject = map(str, table['table_name'].split('_'))
            subquery = "ALTER TABLE {} RENAME {}_{}_{}".format(table['table_name'], new_track, new_year, msubject)
            cursor.execute(subquery)
            db.commit()

        echo(style(' [\u2713] ', fg='green', bold=True) + style('{} {} modified successfully from `{}` alongside all related tables.'.format(track, year , name), bold=True))
    except Error as err:
        echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def track_exists(db, cursor, name, id, year):

    '''
    Search if a track (filiere) already exists.
    '''

    query = "SELECT * FROM {} WHERE id=\'{}\' AND year={}".format(name, id, year)
    cursor.execute(query)
    return cursor.rowcount
