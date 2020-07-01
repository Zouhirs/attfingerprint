#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

@click.group()
@click.option('-s', '--server', '_server', type=str, default='127.0.0.1', nargs=1, help='Server IPv4 address. (Default: 127.0.0.1)')
@click.option('-u', '--user', '_user', type=str, required=True, nargs=1, help='Username.')
@click.option('-b', '--database', '_database', type=str, required=True, nargs=1, help='Database name.')
@click.pass_context
def main(ctx, _server, _user, _database):
	ctx.ensure_object(dict)
	ctx.obj['server'] = _server
	ctx.obj['user'] = _user
	ctx.obj['database'] = _database

def abort_if_false(ctx, param, value):
	if not value:
		ctx.abort()

# ------------------------------------------------------- track ------------------------------------------------------- #

@main.group()
@click.option('-n', '--name', '_name', type=str, default='Tracks', nargs=1, help='Name of table of tracks (Default: Tracks).')
@click.pass_context
def track(ctx, _name):
	ctx.ensure_object(dict)
	ctx.obj['name'] = _name

@track.command()
@click.pass_context
def create(ctx):
	'''
	Create table that contains tracks (Filieres).
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .track import create
		create(db, cursor, ctx.obj['name'])
		cursor.close()
		db.close()

@track.command()
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='Tracks table and all related tables will be deleted. Proceed?')
@click.pass_context
def drop(ctx):
	'''
	Drop tracks (filieres) table and all related tables for every track.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .track import drop
		drop(db, cursor, ctx.obj['name'])
		cursor.close()
		db.close()

@track.command()
@click.option('-t', '--track', '_track', type=str, required=True, nargs=1, help='Academic track.')
@click.option('-y', '--year', '_year', type=int, required=True, nargs=1, help='Academic year of track.')
@click.pass_context
def add(ctx, _track, _year):
	'''
	Add a track (filiere) to the table and create correspondant tables.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .track import add
		add(db, cursor, ctx.obj['name'], _track, _year)
		cursor.close()
		db.close()

@track.command()
@click.pass_context
def list(ctx):
	'''
	Print out all tracks (filieres) available.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .track import list
		list(db, cursor, ctx.obj['name'])
		cursor.close()
		db.close()

@track.command()
@click.option('-t', '--track', '_track', type=str, required=True, nargs=1, help='Academic track.')
@click.option('-y', '--year', '_year', type=int, required=True, nargs=1, help='Academic year of track.')
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='All tables related to this track will be deleted. Proceed?')
@click.pass_context
def delete(ctx, _track, _year):
	'''
	Delete a track (filiere) and all correspondant tables.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .track import delete
		delete(db, cursor, ctx.obj['name'], _track, _year)
		cursor.close()
		db.close()

@track.command()
@click.option('-t', '--track', '_track', type=str, required=True, nargs=1, help='Academic track.')
@click.option('-y', '--year', '_year', type=int, required=True, nargs=1, help='Academic year of track.')
@click.pass_context
def rename(ctx, _track, _year):
	'''
	Rename a track (filiere) and all its correspondant tables name.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .track import rename
		rename(db, cursor, ctx.obj['name'], _track, _year)
		cursor.close()
		db.close()

# ------------------------------------------------------- week ------------------------------------------------------- #

@main.group()
@click.option('-n', '--name', '_name', type=str, default='Weeks', nargs=1, help='Name of table of weeks (Default: Weeks)')
@click.pass_context
def week(ctx, _name):
	ctx.ensure_object(dict)
	ctx.obj['name'] = _name

@week.command()
@click.pass_context
def create(ctx):
	'''
	Create table that contains Weeks (Liste des semaines).
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .week import create
		create(db, cursor, ctx.obj['name'])
		cursor.close()
		db.close()

@week.command()
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='Tracks table and all related tables will be deleted. Proceed?')
@click.pass_context
def drop(ctx):
	'''
	Delete weeks (liste des semaines) table.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .week import drop
		drop(db, cursor, ctx.obj['name'])
		cursor.close()
		db.close()

@week.command()
@click.option('-s', '--start-date', '_start_date', type=str, required=True, nargs=1, help='Start date of the week to add [yyyy-mm-dd].')
@click.option('-e', '--end-date', '_end_date', type=str, required=True, nargs=1, help='End date of the week to add [yyyy-mm-dd].)')
@click.pass_context
def add(ctx, _start_date, _end_date):
	'''
	Add a week info manually.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .week import add
		add(db, cursor, ctx.obj['name'], _start_date, _end_date)
		cursor.close()
		db.close()

@week.command()
@click.option('-s', '--start-date', '_start_date', type=str, required=True, nargs=1, help='Start date of the week to add [yyyy-mm-dd].')
@click.option('-t', '--total', '_total', type=str, required=True, nargs=1, help='Total number of week to add.')
@click.option('-w', '--week-manual', '_week_manual', multiple=True, help='Week(s) to add manually.')
@click.option('-d', '--days-study', '_days_study', type=int, required=True, nargs=1, help='Number of school days.')
@click.pass_context
def addauto(ctx, _start_date, _total, _week_manual, _days_study):
	'''
	Automatically insert weeks with the option of choosing weeks to enter manually.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .week import addauto
		addauto(db, cursor, ctx.obj['name'], _start_date, _total, _week_manual, _days_study)
		cursor.close()
		db.close()

@week.command()
@click.pass_context
def list(ctx):
	'''
	List weeks (liste des semaines).
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .week import list
		list(db, cursor, ctx.obj['name'])
		cursor.close()
		db.close()

@week.command()
@click.option('-m', '--number', '_number', type=int, nargs=1, help='Number of week to modify')
@click.pass_context
def modify(ctx, _number):
	'''
	Modify the start date and/or end date of a week.
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .week import modify
		modify(db, cursor, ctx.obj['name'], _number)
		cursor.close()
		db.close()

# ------------------------------------------------------- subject ------------------------------------------------------- #

@main.group()
@click.option('-t', '--track', '_track', type=str, required=True, nargs=1, help='Name of track of subjects.')
@click.option('-y', '--year', '_year', type=int, required=True, nargs=1, help='Academic year of track of subjects.')
@click.pass_context
def subject(ctx, _track, _year):
	ctx.ensure_object(dict)
	ctx.obj['track'] = _track
	ctx.obj['year'] = _year

@subject.command()
@click.option('-n', '--track-table', '_track_table', type=str, default='Tracks', nargs=1, help='Name of tracks table. (Default: Tracks)')
@click.option('-l', '--number', '_number', type=int, default=1, nargs=1, help='Number of subjects to add.')
@click.pass_context
def add(ctx, _number, _track_table):
	'''
    Add a new subject (module)
    '''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .subject import add
		add(db, cursor, _number, _track_table, ctx.obj['track'], ctx.obj['year'])
		cursor.close()
		db.close()

@subject.command()
@click.option('-c', '--code', '_code', required=True, type=str, nargs=1, help='Subject code.')
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='Subject will be deleted. Continue?')
@click.pass_context
def delete(ctx, _code):
	'''
    Delete a subject (module)
    '''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .subject import delete
		delete(db, cursor, ctx.obj['track'], ctx.obj['year'], _code)
		cursor.close()
		db.close()

@subject.command()
@click.pass_context
def list(ctx):
	'''
	List subjects (modules).
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .subject import list
		list(db, cursor, ctx.obj['track'], ctx.obj['year'])
		cursor.close()
		db.close()

# ------------------------------------------------------- lists ------------------------------------------------------- #

@main.group()
@click.option('-t', '--track', '_track', type=str, required=True, nargs=1, help='Name of track.')
@click.option('-y', '--year', '_year', type=int, required=True, nargs=1, help='Academic year of track.')
@click.pass_context
def lists(ctx, _track, _year):
	ctx.ensure_object(dict)
	ctx.obj['track'] = _track
	ctx.obj['year'] = _year

@lists.command()
@click.pass_context
def generate(ctx):
	'''
	Generate attendance lists (listes de presence) for the track (filiere).
	'''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .lists import generate
		generate(db, cursor, ctx.obj['track'], ctx.obj['year'])
		cursor.close()
		db.close()

@lists.command()
@click.option('--yes', is_flag=True, callback=abort_if_false, expose_value=False, prompt='All attendance lists related to this track will be deleted. Continue?')
@click.pass_context
def drop(ctx):
	'''
    Drop all attendance lists (listes des presences) of a track (filiere)
    '''
	from .connect import connect
	db, cursor = connect(ctx.obj['server'], ctx.obj['user'], ctx.obj['database'])
	if db is not None and cursor is not None:
		from .lists import drop
		drop(db, cursor, ctx.obj['track'], ctx.obj['year'])
		cursor.close()
		db.close()
