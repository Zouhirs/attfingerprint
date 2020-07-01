#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from click import echo, style, clear
from mysql.connector import Error

def generate(db, cursor, track, year):

	'''
	Generate attendance lists (listes de presence) for the track (filiere).
	'''

	# Get subjects
	query = "SELECT `code`, `start_week`, `end_week` FROM {}_{}_Subjects".format(track, year)
	try:
		cursor.execute(query)
		subjects = cursor.fetchall()

		# Create tables for all subjects
		for subject in subjects:
			subquery1 = '''CREATE TABLE {t}_{y}_{} (
				`id` int(4) NOT NULL,
				`first_name` varchar(20) NOT NULL,
				`last_name` varchar(40) NOT NULL,
				PRIMARY KEY (`id`),
				FOREIGN KEY (id) REFERENCES {t}_{y}_Students(id) ON DELETE CASCADE ON UPDATE CASCADE,
				FOREIGN KEY (first_name) REFERENCES {t}_{y}_Students(first_name) ON DELETE CASCADE ON UPDATE CASCADE,
				FOREIGN KEY (last_name) REFERENCES {t}_{y}_Students(last_name) ON DELETE CASCADE ON UPDATE CASCADE
				) ENGINE=InnoDB '''.format(subject['code'], t=track, y=year)

			cursor.execute(subquery1)

			for week in range(subject['start_week'], subject['end_week'] + 1):
				subquery2 = "ALTER TABLE {}_{}_{} ADD `S{}` varchar(2) DEFAULT 'A'".format(track, year, subject['code'], week)
				cursor.execute(subquery2)

			subquery3 = '''INSERT INTO {t}_{y}_{} (id, first_name, last_name)
						SELECT * FROM {t}_{y}_Students'''.format(subject['code'], t=track, y=year)
			cursor.execute(subquery3)
			db.commit()

			echo(style(' [\u2713] ', fg='green', bold=True) + style('Table `{}_{}_{}` created.'.format(track, year, subject['code']), bold=True))

	except Error as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))

def drop(db, cursor, track, year):

	'''
	Drop all attendance lists (listes des presences) of a track (filiere)
	'''

	query1 = "SELECT table_name FROM information_schema.tables WHERE table_name REGEXP \'^{}_{}_M[0-9]+\'".format(track, year)

	try:
		cursor.execute(query1)
		tables = cursor.fetchall()

		for table in tables:
			query2 = "DROP TABLE {}".format(table['table_name'])
			cursor.execute(query2)
			db.commit()
			echo(style(' [\u2713] ', fg='green', bold=True) + style('Table `{}` deleted.'.format(table['table_name']), bold=True))

	except Error as err:
		echo(style(' [x] ', fg='red', bold=True) + style(str(err), bold=True))
