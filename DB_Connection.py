__author__ = 'Kaiqun'

import MySQLdb
import pymssql
import pymongo
import ast
import json
import time
import calendar

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

def MongoDB_Insertion(inputObject, MappingIndex):
	mongodb_uri = 'mongodb://localhost:27017'
	db_name = 'names'

	try:
		connection = pymongo.Connection (mongodb_uri)
		database = connection[db_name]
	except:
		print('Error: Unable to connect to database.')
		connection = None

	if connection is not None:
		for f in inputObject:
			jsonstr = str(f)
			TempJson = json.loads(jsonstr)
			TempJson.update({"_id": TempJson['id']})
			if TempJson.get('urls'):
				TempJson.update({"urls": "ILLEGAL"})
			TempJson.update({"pj_mapping": MappingIndex})
			TempJson.update({"pj_UTCtime": calendar.timegm(time.strptime(TempJson['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))})
			try:
				database.adventurers.insert(TempJson)
			except Exception, e:
				print e.message
				return 'Crap!'
	return 'Done'