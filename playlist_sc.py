# -*- coding: utf-8 -*-
from __future__ import division
import sys
import urllib2
import urllib
import re
from urllib import urlopen
import json 
import difflib
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import time
import soundcloud
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import string	
from collections import defaultdict	
from time import sleep
from collections import defaultdict
from operator import itemgetter
import operator
import datetime
from datetime import datetime

# SoundCloud initialization

client = 'e9254de57c63214abef885f505100d91'	
client_id='client_id=e9254de57c63214abef885f505100d91'
client1 = soundcloud.Client(client_id='e9254de57c63214abef885f505100d91')

i = datetime.now()
def FindDuplicates(in_list):  
    duplicates = []
    unique = set(in_list)
    for each in unique:
        count = in_list.count(each)
        if count >=2:
            duplicates.append(each)
    print duplicates
    return duplicates

# Enter the link of the song you need recommendation on

var = raw_input("Enter your SoundCloud URL: ")
print "Fetching details for ",var	

# # Extracting the track id

resolve="https://api-v2.soundcloud.com/resolve?url=%s&client_id=e9254de57c63214abef885f505100d91" % (var)
resolve=urlopen(resolve).read()
resolve = unicode(resolve, 'latin-1')
resolve=json.loads(resolve)
track_ids=resolve['id']

track_id= []
track_playlist=[]
playlist_id = []
track_list=[]

limit1 = '20'
limit2 = '25'

sc_api1="https://api-v2.soundcloud.com/tracks/%s/playlists?client_id=e9254de57c63214abef885f505100d91&linked_partitioning=1&limit=%s" % (str(track_ids),limit1)
sc_api2="https://api-v2.soundcloud.com/tracks/%s/playlists?client_id=e9254de57c63214abef885f505100d91&linked_partitioning=1&limit=%s" % (str(track_ids),limit2)

try:
	sc_relate=urlopen(sc_api1).read()
except:
		sc_relate=urlopen(sc_api2).read()

sc_relate = unicode(sc_relate, 'latin-1')
sc_relate=json.loads(sc_relate)
for y in sc_relate['collection']:
	        likes_count=y['likes_count']
	        reposts_count=y['reposts_count']
	        permalink_url=y['id']
	        if 5<=likes_count or 2<=reposts_count:
	            playlist_id.append(permalink_url)
	        else:
	            pass

if 'next_href' in sc_relate:
		next_href=sc_relate['next_href']
else:
	next_href=None

while len(playlist_id)<=20:
	print len(playlist_id)
	if next_href is not None:
			print "sleeping for 5 secs"
			
			try:
				next_href_f = next_href+'&'+str(client_id)
				sc_=urlopen(next_href_f).read()
				sc_rel=json.loads(sc_)
				for y in sc_rel['collection']:
				        likes_count=y['likes_count']
				        reposts_count=y['reposts_count']
				        permalink_url=y['id']
				        if 5<=likes_count or 2<=reposts_count:
				            playlist_id.append(permalink_url)
				        else:
				        	pass
				if 'next_href' in sc_rel:
							next_href=sc_rel['next_href']
			except Exception as e:
				print e
	else:
		print("All playlists retrieved")
		break

Final_List = playlist_id
print len(Final_List)

print "Fetching your Playlist Tracks"

idtrack = []
finaldict = {}

for row in Final_List:
	user_1='http://api.soundcloud.com/playlists/'
	user_2=str(row)
	user_3='?client_id='	
	user_4=str(client)
	user_='&format=json'
	user_final=user_1+user_2+user_3+user_4+user_
	user_final=urlopen(user_final).read()	
	user_final=json.loads(user_final)
	for k in user_final['tracks']:
		track_id = k['id']
		duration = k['duration']
		if track_id == track_ids or duration > 720000 :
			pass
		else:
			idtrack.append(track_id)

available_track = FindDuplicates(idtrack)

for row in available_track:
	user_1='http://api.soundcloud.com/tracks/'
	user_2=str(row)
	user_3='?client_id='	
	user_4=str(client)
	user_='&format=json'
	user_final=user_1+user_2+user_3+user_4+user_
	user_final=urlopen(user_final).read()	
	user_final=json.loads(user_final)
	track_id = user_final['id']
	createdtime = user_final['created_at']
	permalink_url=user_final['permalink_url']
	try:
		track_likes=user_final['favoritings_count']
	except:
		track_likes=0
	try:
		track_reposts=user_final['playback_count']
	except:
		track_reposts=1

	ratio = (track_likes)/(track_reposts)
	mdate = createdtime[:19]
	rdate = i.strftime('%Y/%m/%d %H:%M:%S')
	mdate1 = datetime.strptime(mdate, "%Y/%m/%d %H:%M:%S").date()
	rdate1 = datetime.strptime(rdate, "%Y/%m/%d %H:%M:%S").date()
	delta =  abs((mdate1 - rdate1).days)
	final_value = (ratio)/(delta)
	finaldict[track_id] = final_value , permalink_url

sorted_finaldict = sorted(finaldict.items(), key=operator.itemgetter(1), reverse = True)
for row in sorted_finaldict:
	print row[1][1].encode('utf-8')
