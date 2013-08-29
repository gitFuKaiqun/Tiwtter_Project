import twitter
import time
import DB_Connection
import json


TwitterAccountPool = [line.strip() for line in open('TwitterAccountList', 'r')]
KeyWordsList = open('Keywords', 'r').read().split('\t')

MappingMatrix = [[point for point in line.split('\t')] for line in open('destination.txt', 'r')]

AccountToken = 0
KeywordToken = 0
OverAllCount = 0

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
		# if tmp.user.screen_name is 'WTOPtraffic':
		print tmp
		# # TempJson = json.load(tmp)
		# # print TempJson['text']
		# if tmp.geo is not None:
		# 	print tmp.user.name + '  Says: ===>  ' + tmp.text.strip().replace('\n', ' ').replace('\r', ' ')

def outputFile(ApiResult, outputPath):
	WriterFile = open(outputPath, 'a')
	for one in ApiResult:
		WriterFile.write(str(one) + '\n')

def ExtractRecentTweets(api, User_id, since_twtId):
	while True:
		TempRslt = api.GetUserTimeline(user_id=User_id, count=200, max_id=since_twtId)
		if not TempRslt:
			return -1
		outputFile(TempRslt, 'ResentTwt/drgridlock_Recent_Tweets')
		since_twtId = TempRslt[len(TempRslt) - 1].id - 1

def outputDataBase(MethodIndex, ApiResult):
	"""

	:param MethodIndex: set to '0' connect to Microsoft SQL Server; set to '1' connect to MySQL Server
	"""
	if MethodIndex is 0:
		DB_Connection.MS_SqlServer_Method(ApiResult)
	elif MethodIndex is 1:
		DB_Connection.MY_SQL_Method(ApiResult)
	else:
		print 'DB connection doesn\'t exist'

def TwitterCrawling():
	"""
	This function enables crawling Tweets with a list of Twitter application accounts and a keywords list.

	"""
	global AccountToken
	global KeywordToken
	global OverAllCount
	while True:
		try:
			TwitterApiInstance = NextAccount(AccountToken)
			OverAllCount = 0
			for y in xrange(len(MappingMatrix)):
				for x in xrange(len(MappingMatrix[y])):
					Xcordi = MappingMatrix[y][x].strip().split(',')[0]
					Ycordi = MappingMatrix[y][x].strip().split(',')[1]
					while True:
						temp = TwitterApiInstance.GetSearch(term=KeyWordsList[KeywordToken], count=100, geocode=(Xcordi,Ycordi,'20mi'))
						# temp = TwitterApiInstance.GetUserTimeline(user_id=217510835, count=1200, max_id=369602873770143746)
						# ExtractRecentTweets(TwitterApiInstance, 18025557, None)
						# return 0
						KeywordToken = (KeywordToken + 1) % len(KeyWordsList)
						time.sleep(0.1)
						# outputConsole(temp)
						DB_Connection.MongoDB_Insertion(temp, [y,x])
						OverAllCount += 1

		except Exception, e:
			global OverAllCount
			if e.__class__.__name__ is 'TwitterError':
				Errotype = e.message[0]['code']
				if Errotype is 88:
					AccountToken = (AccountToken + 1) % AccCount()
					print 'Switch Account! Next Account:' + str(AccountToken) + '  Total queries sent:' + str(OverAllCount)
				else:
					print e
			else:
				print "SERIOUS ERROR! ======> " + e.message

if  __name__ == '__main__':
	print TwitterCrawling()