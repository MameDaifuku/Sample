# -*- coding: utf-8 -*-
import sys
import os
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint

sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "/../..")
from common.src import utility
################################################
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
headers = {'User-Agent' : USER_AGENT, "Content-Type" : "application/json"}

def run():
	# channel_id = "UCfQVs_KuXeNAlGa3fb8rlnQ" # りつきん
	# channel_id = "UCCebCRguPlkvWemz2dKxWIA" # キルシュトルテ
	channel_id = "UCjXBuHmWkieBApgBhDuJMMQ" # 八雲べに
	
	first_token = get_first_token(channel_id)
	
	if first_token != "" :
		next_token = first_token
		for i in range(10):
			print("▼▼▼▼▼▼ループ Start▼▼▼▼▼▼▼")
			next_token = print_video_info_and_get_next_token(next_token)
			print("next_token = " + next_token)

			if (next_token == "") :
				print("breeeeeeeeeeeeeeak")
				break
			###

			print("▲▲▲▲▲▲▲▲ループ End▲▲▲▲▲▲▲▲▲")
		###
	###
###

def print_video_info_and_get_next_token(token) :
	
	result = ""

	url = "https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
	payload = {
		"context": {
			"client": {
				"clientName": "WEB",
				"clientVersion": "2.20211119.01.00",
			},
		},
		"continuation":token
	}

	html = requests.post(url, headers=headers, data=json.dumps(payload))
	j = json.loads(html.text)
	print("★continuationItem count = " + str(len(j["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"])) + "★")
	for continuationItem in j["onResponseReceivedActions"][0]["appendContinuationItemsAction"]["continuationItems"]:
		if "gridVideoRenderer" in continuationItem:
			gridVideoRenderer = continuationItem["gridVideoRenderer"]
			video_id = gridVideoRenderer["videoId"]
			video_title = gridVideoRenderer["title"]["runs"][0]["text"]
			# published_at = get_published_at(video_id)
			duration = do_format_duration(gridVideoRenderer["thumbnailOverlays"][0]["thumbnailOverlayTimeStatusRenderer"]["text"]["simpleText"])

			# print(video_id)
			print(video_title)
			# print(published_at)
			print(duration)
		else :
			result = continuationItem["continuationItemRenderer"]["continuationEndpoint"]["continuationCommand"]["token"]
		###
	###

	return result
###

def do_format_duration(origin) :
	result = ""

	# hh:mm:ss形式に補正する
	if len(origin) == 7 : #sample 1:23:45
		result = "0" + origin
	elif len(origin) == 5 : #sample 23:45
		result = "00:" + origin
	elif len(origin) == 4 : #sample 3:45
		result = "00:0" + origin
	elif len(origin) == 2 : #sample 45
		result = "00:00:" + origin
	elif len(origin) == 1 : #sample 5
		result = "00:00:0" + origin
	###

	return result
###

def get_published_at(video_id) :
	url = f"https://www.youtube.com/watch?v={video_id}"
	html = requests.get(url)
	temp = html.text.split("\"uploadDate\":\"")[1]
	temp = temp.split("\"")[0]
	
	return temp
###

def get_first_token(channel_id) :
	result = ""

	url = f"https://www.youtube.com/channel/{channel_id}/videos"
	html = requests.get(url)
	temp = html.text.split("var ytInitialData = ")[1]
	temp = temp.split(";</script>")[0]
	items = json.loads(temp) \
		["contents"] \
		["twoColumnBrowseResultsRenderer"] \
		["tabs"] \
		[1] \
		["tabRenderer"] \
		["content"] \
		["sectionListRenderer"] \
		["contents"] \
		[0] \
		["itemSectionRenderer"] \
		["contents"] \
		[0] \
		["gridRenderer"] \
		["items"]

	for item in items :
		if "continuationItemRenderer" in item : 
			result = item \
				["continuationItemRenderer"] \
				["continuationEndpoint"] \
				["continuationCommand"] \
				["token"]
		###
	###

	return result
###

run()