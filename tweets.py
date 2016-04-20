#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#------------------------------------------------------------------------------------
#--------------------------------------HEADER----------------------------------------
#	Author: 		Tibor Dudlák	
#	Login: 			xdudla00	
#	Mail: 			xdudla00@stud.fit.vutbr.cz
#	Description:	tweets downloader in python
#------------------------------------------------------------------------------------
#------------------------------------LIBRARIES---------------------------------------
import os 						# work with filesystem
import csv						# writing to file format *.csv 
import sys						# command line arguments
import tweepy					# work with tweets
import urllib3					# work with urls
import requests					# downloading content of links
from collections import deque	# reading from last line
#---------------------------------------KEYS-----------------------------------------
consumer_key 		= 'FjaF2bSXGvDxnR4nhrG4iGUgD'
consumer_secret 	= 'l57Xf391y8H4ZREutdG6Y82Mb70jrliNRBWXLkbV3effi0XCT6'
access_token  		= '2426806712-BAUFr45f1qO6iU9S3MscfLPAiN3sLECVihxrmRZ'
access_token_secret	= 'Y3p8jyDII4tiOIIfgdphVza6ewI2cyYE7iywZMUwWZSnR'
#----------------------------------AUTHENTIFICATION----------------------------------
auth = tweepy.OAuthHandler ( consumer_key, consumer_secret )
auth.set_access_token ( access_token, access_token_secret )
api = tweepy.API ( auth )
#-------------------------------------FUNCTIONS--------------------------------------

def get_tweets_update ( account ) : 	
	
	row = deque ( csv.reader ( open ( '%s_tweets.csv' % account, 'r' ) ) ,1 ) [0]
	latest = row [0]
	tweets = api.user_timeline ( screen_name = account, since_id = latest , count = 200)
	if ( len ( tweets ) == 0 ):
		print "nothing to do, all tweets are up to date"
		return
		# in fact... it ends program
	print "updating tweets..."
	tweets.reverse ()
	all_tweets = [ [ tweet.id_str, tweet.created_at, tweet.text.encode("utf-8") ] for tweet in tweets ]
	with open ( '%s_tweets.csv' % account, 'ab' ) as f:
		writer = csv.writer ( f )
		writer.writerows ( all_tweets )
	if ( len ( all_tweets ) == 1 ):
		print "latest tweet downloaded"
	else:
		print "%d latest tweets downloaded" % len ( all_tweets )
	download_sites ( tweets , account )

#------------------------------------------------------------------------------------

def get_tweets_new ( account ) :		
	
	try:
		print "downloading tweets..."
		tweets = api.user_timeline ( screen_name = account , count = 50 )
	except:
		print "account does not exists"
		return
	tweets.reverse ()
	all_tweets = [ [ tweet.id_str, tweet.created_at, tweet.text.encode ( "utf-8" ) ] for tweet in tweets ]
	with open ( '%s_tweets.csv' % account, 'wb' ) as f:
		writer = csv.writer ( f )
		writer.writerow ( ["id","created_at","text"] )
		writer.writerows ( all_tweets )
	print "%d latest tweets downloaded" % len ( all_tweets )
	download_sites ( tweets , account )	

#------------------------------------------------------------------------------------

def download_sites ( tweets , account ):	
	
	print "downloading extern link content, please wait..."
	my_dir=account+'_sites'
	if ( not os.path.exists ( my_dir ) ) :
		os.makedirs ( my_dir ) 
	for tweet in tweets:
		for data in tweet.entities [ 'urls' ] :
			link = data [ 'expanded_url' ]
			site = requests.get ( link )
			filename = str (tweet.created_at)+' '+str ( link.split ( '/' ) [-1] )+'_.html'
			# name contains date and time of tweet plus last characters after '/' from link
			with open ( os.path.join ( my_dir, filename ), 'wb' ) as temp_file:
				temp_file.write ( site.content )
	print "download complete"

#-----------------------------MAIN_FUNCTION------------------------------------------

if __name__ == '__main__':
	try:
		if ( os.path.isfile ( '%s_tweets.csv' % sys.argv[1] ) ):
			get_tweets_update ( sys.argv[1] )	
			# sys.argv[1] holds first argument from command line
		else:
			get_tweets_new ( sys.argv[1] ) 		
			# this argument should be twitter account name to download
	except:
		print "program argument supose to be twitter account name"

#-------------------------------------------------------------------------------------