#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from pyfingerprint.pyfingerprint import PyFingerprint

@click.group()
@click.option('-s', '--server', '_server', type=str, default='127.0.0.1', nargs=1, help='Server IPv4 address. (Default: 127.0.0.1)')
@click.option('-u', '--user', '_user', type=str, required=True, nargs=1, help='Username.')
@click.option('-b', '--database', '_database', type=str, required=True, nargs=1, help='Database name.')
@click.option('-t', '--track', '_track', type=str, required=True, nargs=1, help='Academic track.')
@click.option('-y', '--year', '_year', type=int, required=True, nargs=1, help='Academic year of track.')
@click.option('-d', '--device', '_device', type=click.Path(exists=True), required=True, nargs=1, help='Sensor\'s file in /dev. (/dev/ttyUSB*)')
@click.pass_context
def main(ctx, _server, _user, _database, _track, _year, _device):
	ctx.ensure_object(dict)
	ctx.obj['server'] = _server
	ctx.obj['user'] = _user
	ctx.obj['database'] = _database
	ctx.obj['track'] = _track
	ctx.obj['year'] = _year
	ctx.obj['device'] = _device

def abort_if_false(ctx, param, value):
	if not value:
		ctx.abort()

@main.command()

@click.option('-n', '--number', '_number', type=int, nargs=1, default=1, help='Number of students to enroll at once. (Default: 1)')
@click.pass_context
def enroll(ctx, _number):
	'''
	Enroll student.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	_fsensor = init(ctx.obj['device'])
	if db is not None and cursor is not None and _fsensor is not None:
		from .enroll import enroll
		enroll(db, cursor, _fsensor, ctx.obj['track'], ctx.obj['year'], _number)
		cursor.close()
		db.close()

@main.command()
@click.pass_context
def list(ctx):
	'''
	Print out list of enrolled student for provided track.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	_fsensor = init(ctx.obj['device'])
	if db is not None and cursor is not None and _fsensor is not None:
		from .list import list
		list(db, cursor, _fsensor, ctx.obj['track'], ctx.obj['year'])
		cursor.close()
		db.close()

@main.command()
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='This will delete a or all sensor\'s stored data. Proceed?')
@click.option('--all', is_flag=True, help='Delete all data in the sensor and file. (Proceed with caution !)')
@click.pass_context
def delete(ctx, all):
	'''
    Delete a Student / All Students From Sensor and File.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	_fsensor = init(ctx.obj['device'])
	if db is not None and cursor is not None and _fsensor is not None:
		from .delete import delete, delete_all
		if all: delete_all(db, cursor, _fsensor, ctx.obj['track'], ctx.obj['year'])
		else : delete(db, cursor, _fsensor, ctx.obj['track'], ctx.obj['year'])
		cursor.close()
		db.close()

@main.command()
@click.pass_context
def search(ctx):
	'''
	Search for student info from fingerprint.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	_fsensor = init(ctx.obj['device'])
	if db is not None and cursor is not None and _fsensor is not None:
		from .search import search
		search(db, cursor, _fsensor, ctx.obj['track'], ctx.obj['year'])
		cursor.close()
		db.close()


def init(device):
	baudrate = 57600
	address = 0xFFFFFFFF
	password = 0x00000000
	fsensor = PyFingerprint(device, baudrate, address, password)

	if not fsensor.verifyPassword(): raise Exception('Sensor\'s password is incorrect.')

	return fsensor
