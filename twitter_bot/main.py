# -*- coding: utf-8 -*-

import os
from pprint import pprint
import time
import datetime
import json, config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

def default_method(item):
	if isinstance(item, object) and hasattr(item, '__dict__'):
		return item.__dict__
	else:
		raise TypeError
	###
###

def get_twitter() :
	return OAuth1Session(
		config.API_KEY,
		config.API_KEY_SECRET,
		config.ACCESS_TOKEN,
		config.ACCESS_TOKEN_SECRET
	)
###

def get_timeline() :
	twitter = get_twitter()
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json" 
	params = {
		'count' : 5
	} 
	
	res = twitter.get(url, params = params)
	
	#リクエスト可能残数の取得
	limit = res.headers['x-rate-limit-remaining'] 
	#リクエスト可能残数リセットまでの時間(UTC)
	reset = res.headers['x-rate-limit-reset'] 
	#UTCを秒数に変換
	sec = int(res.headers['X-Rate-Limit-Reset']) - time.mktime(datetime.datetime.now().timetuple()) 

	print ("━━━━━━━━━━━━━━━━━━━━━━━━")
	print ("limit: " + limit)
	print ("reset: " +  reset)
	print ('reset sec:  %s' % sec)
	print ("━━━━━━━━━━━━━━━━━━━━━━━━")

	if res.status_code == 200: 
		timelines = json.loads(res.text)
		for line in timelines:
			print(line['user']['name']+'::'+line['text'])
			print(line['created_at'])
			print('*******************************************')
		###
	else: 
		print("Failed: %d" % res.status_code)
	###
###

def post_tweet(twitter_status_id, twitter_screen_name) :
	twitter = get_twitter()
	url = "https://api.twitter.com/1.1/statuses/update.json" 
	tweet_status = "" # 	ツイート内容
	if twitter_status_id != "" : 
		# リプライ先ツイートが指定されている場合、メンション先を指定する必要あり。
		tweet_status += f"@{twitter_screen_name} " 
	###
	tweet_status += datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "なう"
	params = {
		"status" : tweet_status,
		"in_reply_to_status_id" : twitter_status_id,
	}
	
	res = twitter.post(url, params = params) 
	if res.status_code == 200: 
		print("Success.")
	else: 
		print("Failed. : %d"% res.status_code)
###

def get_rate_limit_status() :
	twitter = get_twitter()	
	url = "https://api.twitter.com/1.1/application/rate_limit_status.json" 
	params = {
		'resources' : "search,statuses" # 指定したリソースの情報だけ取得する。未指定の場合は全リソースの情報を取得する。
# 		'resources' : "search,statuses,favorites,followers,friends,friendships"
	} 
	
	res = twitter.get(url, params = params)
	if res.status_code == 200: 
		pprint(json.loads(res.text))
	else: 
		print("Failed: %d" % res.status_code)
	###
###

def get_search_result() :
	twitter = get_twitter()
	url = "https://api.twitter.com/1.1/search/tweets.json" 
	query_word = "グラブル "
	query_from = f"from:{config.twitter_screen_name} "
	query_since = "since:2020-11-01 "
	query_until = "until:2020-12-31 "
	query_filter = "-filter:retweets " 
	query_combined = ""
	query_combined += query_word
	query_combined += "OR @toooooooooooooooooos"
# 	query_combined += query_from
# 	query_combined += query_since
# 	query_combined += query_until
	query_combined += query_filter
	params = {
		"q" : query_combined,
		"count" : 10,
		"result_type" : "recent",
	} 
	
	res = twitter.get(url, params = params)
	if res.status_code == 200: 
		max_id = 0
		min_id = 99999999999999999999
		result = []
		res_json = json.loads(res.text)
		for tweet in res_json["statuses"]:
# 			pprint(tweet)
# 			print(tweet["created_at"])
# 			print(tweet["id"])
# 			print(tweet["user"]["name"])
# 			print(tweet["text"])
# 			print('*******************************************')

			# result_typeがrecentなら結果が降順で返ってくるので最初と最後の値を取れば済む
			if max_id < tweet["id"] : max_id = tweet["id"]
			if min_id > tweet["id"] : min_id = tweet["id"]
			
			temp = {}
			temp["created_at"] = tweet["created_at"]
			temp["id"] = tweet["id"]
			temp["screen_name"] = tweet["user"]["name"]
			temp["text"] = tweet["text"]
			result.append(temp)
		###
		
		file_path = f"{dir_path_output}/{min_id}_{max_id}.json"
		with open(file_path, mode="w", encoding="utf-8_sig") as f:
			f.write(json.dumps(result, default=default_method, ensure_ascii=False, indent=4))
			###
		###
		
		print(json.dumps(result, default=default_method, ensure_ascii=False, indent=4))
	else: 
		print("Failed: %d" % res.status_code)
	###
###

def post_favorite(method) :
	twitter = get_twitter()
	url = f"https://api.twitter.com/1.1/favorites/{method}.json" 
	params = {
		"id" : config.twitter_status_id,
	}
	
	res = twitter.post(url, params = params) 
	if res.status_code == 200: 
		print("Success.")
		pprint(json.loads(res.text))
	else: 
		print("Failed. : %d"% res.status_code)
###

def post_retweet(method) :
	twitter = get_twitter()
	url = f"https://api.twitter.com/1.1/statuses/{method}/{config.twitter_status_id}.json" 
	res = twitter.post(url) 
	
	if res.status_code == 200: 
		print("Success.")
		pprint(json.loads(res.text))
	else: 
		print("Failed. : %d"% res.status_code)
###

def post_friendships(method) :
	twitter = get_twitter()
	url = f"https://api.twitter.com/1.1/friendships/{method}.json" 
	params = {
		"screen_name" : config.twitter_screen_name, 
	}

	res = twitter.post(url, params = params) 
	if res.status_code == 200: 
		print("Success.")
		pprint(json.loads(res.text))
	else: 
		print("Failed. : %d"% res.status_code)
###

def post_direct_messages(method) :
	twitter = get_twitter()
	url = f"https://api.twitter.com/1.1/direct_messages/events/{method}.json" 
	headers = {"content-type": "application/json"}
	params = {
		"event" : {
			"type" : "message_create",
			"message_create" : {
				"target": {
					"recipient_id": config.twitter_user_id 
				}, 				
				"message_data": {
					"text": "これはDMの本文です。"
				} 
			}
		}
	}

	#headersにはdictではなくstrを渡しましょう
	res = twitter.post(url, headers=headers, data=json.dumps(params))  
	if res.status_code == 200: 
		print("Success.")
		pprint(json.loads(res.text))
	else: 
		print("Failed. : %d"% res.status_code)
	###
###


####################################################
def run():
# 	post_tweet("", "") #通常のツイート
# 	post_tweet(config.twitter_status_id, config.twitter_screen_name) # 特定のツイートに対するリプライ
# 	get_timeline() #タイムライン取得
# 	get_rate_limit_status() #APIの利用上限に関する情報の取得
	get_search_result() #検索実行
# 	post_favorite("create") # いいね実行（連続実行するとエラー）
# 	post_favorite("destroy") # いいね解除（連続実行するとエラー）
# 	post_retweet("retweet") # リツイート実行（連続実行するとエラー）
# 	post_retweet("unretweet") # リツイート解除（連続実行するとエラー）
# 	post_friendships("create") #フォロー実行
# 	post_friendships("destroy") # フォロー解除
# 	post_direct_messages("new") #DM送信
	
####################################################
dir_path_output = "./output"
if not os.path.exists(dir_path_output) : os.mkdir(dir_path_output) #get_search_resultで結果をファイル出力

run()