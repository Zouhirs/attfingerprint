#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import mysql.connector as mysql
from click import echo, style, clear
from getpass import getpass

def connect(host, user, database):
    '''
    Connect to database.
    '''
    valid_ip = validateIPaddress(host)
    if not valid_ip:
        echo(style(' [x] ', fg='red', bold=True) + style('IP address invalid.\n', bold=True))
        return 1
    password = getpass(style(' [?] ', fg='yellow', bold=True) + style('Enter server\'s password for user ', bold=True) + style(user, fg='green') + ': ')
    try:
        db, cursor = establish(host, user, password, database)
        echo(style(' [\u2713] ', fg='green', bold=True) + style('Connected to database.', bold=True))
        return db, cursor
    except mysql.Error as err:
        if err.errno == 2003 : error_msg = 'Can\'t connect to provided server address. Please check again.'
        elif err.errno == 1045 : error_msg = 'Username or password incorrect.'
        elif err.errno == 1049 : error_msg = 'Database provided does not exist.'
        else : error_msg = 'Some error occured. Please try again.' + str(err)
        echo(style(' [x] ', fg='red', bold=True) + style(error_msg, bold=True))
        return None, None

def validateIPaddress(address):
    '''
    Validate IP Address Format using Regex.
    '''
    if address == 'localhost': return True
    regex_ip = '(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))'
    validate = re.match(regex_ip, address)
    return validate

def establish(host, username, password, database):
    '''
    Connect to Server's Database.
    '''
    db = mysql.connect(host=host, user=username, password=password, database=database, connection_timeout=4)
    cursor = db.cursor(buffered=True, dictionary=True)
    return db, cursor
