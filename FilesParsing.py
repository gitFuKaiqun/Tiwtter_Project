__author__ = 'Kaiqun'

import os
import json

def processing(path):
	files = os.listdir(path)
	for f in files:
		readingFile = open(path + '/' + f)
		for l in readingFile:
			WritingFile = open('TextResult/' + f, 'a')
			stringuft8 = json.loads(l)['text'].encode('UTF-8')
			WritingFile.write(stringuft8 + '\n')
		# TweetTextContenList = [json.loads(l)['text'] for l in readingFile]
		# print TweetTextContenList
	return 'done'

if __name__=='__main__':
	print processing('ResentTwt')