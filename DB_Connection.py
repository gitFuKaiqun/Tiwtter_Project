__author__ = 'Kaiqun'

import MySQLdb
import pymssql

Connection_Config = [line.strip() for line in open('Connections', 'r')]

def MS_SqlServer_Method(ApiResult):
	"""


	"""
	conn = pymssql.connect(
		host=Connection_Config[0].split('\t')[0],
		user=Connection_Config[0].split('\t')[1],
		password=Connection_Config[0].split('\t')[2],
		database=Connection_Config[0].split('\t')[3]
	)
	cur = conn.cursor()

	cur.execute('SELECT TOP 1000 * FROM [snaps].[dbo].[vw_getACISA]')

	row = cur.fetchone()
	while row:
		print "ID=%d" % (row[0])
		row = cur.fetchone()

def MY_SQL_Method(ApiResult):
	"""


	"""
	conn = MySQLdb.connect(
		host=Connection_Config[1].split('\t')[0],
		user=Connection_Config[1].split('\t')[1],
		passwd=Connection_Config[1].split('\t')[2],
		db=Connection_Config[1].split('\t')[3]
	)