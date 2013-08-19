import twitter
import time
import DB_Connection
import ast

TwitterAccountPool = [line.strip() for line in open('TwitterAccountList', 'r')]
KeyWordsList = open('Keywords', 'r').read().split('\t')

AccountToken = 0
KeywordToken = 0

def NextAccount(AccNum):
	api = twitter.Api(
	    consumer_key=TwitterAccountPool[AccNum].split('\t')[0],
	    consumer_secret=TwitterAccountPool[AccNum].split('\t')[1],
	    access_token_key=TwitterAccountPool[AccNum].split('\t')[2],
	    access_token_secret=TwitterAccountPool[AccNum].split('\t')[3]
	)
	return api

def AccCount():
	count = 0
	thefile = open('TwitterAccountList', 'rb')
	while 1:
		buffer = thefile.read(65536)
		if not buffer:break
		count += buffer.count('\n')
	return count + 1

def outputConsole(ApiResult):
	for tmp in ApiResult:
		if tmp.geo is not None:
			print tmp.geo

def outputFile(ApiResult):
	WriterFile = open('', 'a')

def outputDataBase(MethodIndex):
	"""

	:param MethodIndex: set to '0' connect to Microsoft SQL Server; set to '1' connect to MySQL Server
	"""
	if MethodIndex is 0:
		DB_Connection.MS_SqlServer_Method()
	elif MethodIndex is 1:
		DB_Connection.MY_SQL_Method()
	else:
		print 'DB connection doesn\'t exist'

def TwitterCrawling():
	"""
	This function enables crawling Tweets with a list of Twitter application accounts and a keywords list.

	"""
	global AccountToken
	global KeywordToken
	while True:
		try:
			TwitterApiInstance = NextAccount(AccountToken)
			while True:
				temp = TwitterApiInstance.GetSearch(term=KeyWordsList[KeywordToken], geocode=(38.907231,-77.036483,'20mi'))
				KeywordToken = (KeywordToken + 1) % len(KeyWordsList)
				time.sleep(0.1)
				outputConsole(temp)

		except Exception, e:
			if e.__class__.__name__ is 'TwitterError':
				Errotype = e.message[0]['code']
				if Errotype is 88:
					AccountToken = (AccountToken + 1) % AccCount()
					print 'Switch Account!'
				else:
					print e
			else:
				print "SERIOUS ERROR! ======> " + e.message

if  __name__ == '__main__':
	TwitterCrawling()