# -*- coding: utf-8 -*-

import time
from pprint import pprint
from bs4 import BeautifulSoup
import json
import requests
import inspect
import os
import glob
import pathlib
import re
import logging

######################################################################
RENDERER_TYPE_NONE = ""#指定なし
RENDERER_TYPE_NORMAL = "liveChatTextMessageRenderer"#通常コメント
RENDERER_TYPE_SUPERCHAT = "liveChatPaidMessageRenderer"#スパチャ
RENDERER_TYPE_NEW_MEMBER_OLD = "liveChatLegacyPaidMessageRenderer"#新規メンバー追加（旧？）
RENDERER_TYPE_NEW_MEMBER = "liveChatMembershipItemRenderer"#新規メンバー追加
RENDERER_TYPE_ROWSPEED1 = "liveChatModeChangeMessageRenderer"#低速モード通知1
RENDERER_TYPE_ROWSPEED2 = "liveChatRestrictedParticipationRenderer"#低速モード通知2
RENDERER_TYPE_STICKER = "liveChatPaidStickerRenderer"#ステッカー

TOP_CONTINUATION = 1
ALL_CONTINUATION = 2
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
headers = {'User-Agent' : USER_AGENT}

######################################################################

class ChatReplay():
	def __init__(
		self,
		exec_target_continuation,
		renderer_type,
		id,
		author_name,
		author_external_channel_id,
		author_badges,
		is_owner,
		is_moderator,
		is_member,
		member_tooltip,
		member_badge_image,
		text,
		purchase_amount_text,
		currency,
		amount,
		timestamp_usec,
		# timestampText,
		video_offset_time_msec):
		
		self.exec_target_continuation = exec_target_continuation
		self.renderer_type = renderer_type
		self.id = id
		self.author_name = author_name
		self.author_external_channel_id = author_external_channel_id
		self.author_badges = author_badges
		self.is_owner = is_owner
		self.is_moderator = is_moderator
		self.is_member = is_member
		self.member_tooltip = member_tooltip
		self.member_badge_image = member_badge_image
		self.text = text
		self.purchase_amount_text = purchase_amount_text
		self.currency = currency
		self.amount = amount
		self.timestamp_usec = timestamp_usec
		# self.timestampText = timestampText
		self.video_offset_time_msec = video_offset_time_msec
###

######################################################################

def default_method(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError
###

def get_first_continuation(video_id, get_target_continuation):
	result = ""
	video_url = f"https://www.youtube.com/watch?v={video_id}&has_verified=1"
	html = requests.get(video_url)
	soup = BeautifulSoup(html.text, "html.parser")

	result = re.findall(r"\"op2[a-zA-Z0-9_]+", html.text)[2].replace("\"", "") + "%3D%3D"

	return result
###

def get_chat_replay_hundler(video_id, exec_target_continuation):
	next_continuation = "dummy"
	for p in range(5):
		try:
			for q in range(5000):
				next_continuation = get_chat_replay(video_id, exec_target_continuation)
				if next_continuation == "":
					break
				else:
					exec_target_continuation = next_continuation
				###
			###
			break
		except KeyError as e:
			if p == 4 : 
				raise e
			else:
				time.sleep(3)
				continue
			###
		###
	###
###

def return_renderer(item):
	renderer_type = ""
	result = ""
	###
	if   RENDERER_TYPE_NORMAL         in item :renderer_type = RENDERER_TYPE_NORMAL#通常コメント
	elif RENDERER_TYPE_SUPERCHAT      in item :renderer_type = RENDERER_TYPE_SUPERCHAT#スパチャ
	elif RENDERER_TYPE_NEW_MEMBER_OLD in item :renderer_type = RENDERER_TYPE_NEW_MEMBER_OLD#新規メンバー追加（旧？）
	elif RENDERER_TYPE_NEW_MEMBER     in item :renderer_type = RENDERER_TYPE_NEW_MEMBER#新規メンバー追加
	elif RENDERER_TYPE_ROWSPEED1      in item :renderer_type = RENDERER_TYPE_ROWSPEED1#低速モード通知1
	elif RENDERER_TYPE_ROWSPEED2      in item :renderer_type = RENDERER_TYPE_ROWSPEED2#低速モード通知2
	elif RENDERER_TYPE_STICKER        in item :renderer_type = RENDERER_TYPE_STICKER#ステッカー
	###
	if renderer_type != "":
		result = item[renderer_type]
		result["rendererType"] = renderer_type
	###
	return result
###

def create_chat_replay_instance(exec_target_continuation, action, renderer):
	text = ""
	if renderer["rendererType"] == "liveChatPaidStickerRenderer" : text += "[ステッカー]"
	if renderer["rendererType"] == "liveChatMembershipItemRenderer" : text += "[新規メンバー]"
	if "message" in renderer:
		for run in renderer["message"]["runs"]:
			if "text" in run:text += run["text"]
			if "emoji" in run:text += "["+run["emoji"]["searchTerms"][0]+"]"
		###
	###

	# 低速モード通知
	if "text" in renderer : text += renderer["text"]["runs"][0]["text"]
	if "subtext" in renderer : 
		for tmp in renderer["subtext"]["runs"] :
			text += tmp["text"]
		###
	###

	author_name = ""
	author_external_channel_id = ""
	if (renderer["rendererType"] == RENDERER_TYPE_ROWSPEED1) or (renderer["rendererType"] == RENDERER_TYPE_ROWSPEED2) : 
		author_name = "低速モード通知"
		author_external_channel_id = ""
	else : 
		author_name = renderer["authorName"]["simpleText"]
		author_external_channel_id = renderer["authorExternalChannelId"]
	###
	author_badges = ""
	is_owner = False
	is_moderator = False
	is_member = False
	member_tooltip = ""
	member_badge_image = ""
	if "authorBadges" in renderer:
		author_badges = renderer["authorBadges"]#TODO メンテ
		for badge in author_badges:
			# print(badge)
			if badge["liveChatAuthorBadgeRenderer"]["tooltip"] == "所有者":
				is_owner = True
			###
			if badge["liveChatAuthorBadgeRenderer"]["tooltip"] == "モデレーター":
				is_moderator = True
			###
			if "メンバー" in badge["liveChatAuthorBadgeRenderer"]["tooltip"]:
				is_member = True
				member_tooltip = badge["liveChatAuthorBadgeRenderer"]["tooltip"]

				# メンバーに対してバッジが設定されてないパターンがある（ex. 卯月コウの新規メンバー）
				if "customThumbnail" in badge["liveChatAuthorBadgeRenderer"] :
					member_badge_image = badge["liveChatAuthorBadgeRenderer"]["customThumbnail"]["thumbnails"][0]["url"]
			###
		###
	###
	purchase_amount_text = ""
	amount = ""
	currency = ""
	if "purchaseAmountText" in renderer:
		purchase_amount_text = renderer["purchaseAmountText"]["simpleText"].replace(",", "")
		#正規表現
		pattern=r'([+-]?[0-9]+\.?[0-9]*)'
		#検索テキスト
		amount = re.findall(pattern, purchase_amount_text)[0]
		currency = purchase_amount_text.replace(str(amount), "")
		# print(currency)
	###

	cr = ChatReplay(
		exec_target_continuation,
		renderer["rendererType"],
		renderer["id"],
		author_name,
		author_external_channel_id,
		author_badges,
		is_owner,
		is_moderator,
		is_member,
		member_tooltip,
		member_badge_image,
		text,
		purchase_amount_text,
		currency,
		amount,
		renderer["timestampUsec"],
		# renderer["timestampText"]["simpleText"],#アーカイブ開始から何分。新規メンバー通知は値保持なし。videoOffsetTimeMsecでフォローできるので無視する。
		action["replayChatItemAction"]["videoOffsetTimeMsec"])
		
	return cr
###

def output_chat_replay_continuation_file(video_id, exec_target_continuation, cr_list):
	video_offset_time_msec_start = cr_list[0].video_offset_time_msec.zfill(10)
	video_offset_time_msec_end = cr_list[-1].video_offset_time_msec.zfill(10)
	
	file_path = f"./output/{video_id}/chat_replay_continuation/{video_offset_time_msec_start}-{video_offset_time_msec_end}.json"
	with open(file_path, mode="w", encoding="utf-8_sig") as f:
		f.write(json.dumps(cr_list, default=default_method, ensure_ascii=False, indent=4))
###

def get_chat_replay(video_id, exec_target_continuation):
	if exec_target_continuation == "" : return
	
	try :
		chat_url = f"https://www.youtube.com/live_chat_replay/get_live_chat_replay?continuation={exec_target_continuation}&pbj=1"
		html = requests.get(chat_url, headers=headers)
		chat_replay_json = json.loads(html.text)
		###
		if "actions" not in chat_replay_json["response"]["continuationContents"]["liveChatContinuation"]:return ""
		###
		actions = chat_replay_json["response"]["continuationContents"]["liveChatContinuation"]["actions"]
		###
		cr_list = []
		for action in actions:
			if action == actions[0]:continue
			if "addChatItemAction" not in action["replayChatItemAction"]["actions"][0]:continue #addLiveChatTickerItemActionを回避（チャットの上に出るスパチャ残滓表示のヤツ）
			###
			renderer = return_renderer(action["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"])
			if renderer == "":continue
			###
			cr_list.append(create_chat_replay_instance(exec_target_continuation, action, renderer))
		###
		if (len(cr_list) > 0) :
			output_chat_replay_continuation_file(video_id, exec_target_continuation, cr_list)
	except Exception as e:
		raise e
	###

	return get_next_continuation(chat_replay_json)
###

def get_next_continuation(chat_replay_json):
	temp = chat_replay_json \
			["response"] \
			["continuationContents"] \
			["liveChatContinuation"] \
			["continuations"] \
			[0] 

	if "liveChatReplayContinuationData" in temp:
		return chat_replay_json \
			["response"] \
			["continuationContents"] \
			["liveChatContinuation"] \
			["continuations"] \
			[0] \
			["liveChatReplayContinuationData"] \
			["continuation"]
	else :
		return ""
	###
###

def get_youtube_chat_replay() :
	video_id = "tM4I4_ZvYCE"
	dir_path_output = "./output"
	dir_path_video_id = f"{dir_path_output}/{video_id}"
	dir_path_chat_replay_continuation = f"{dir_path_video_id}/chat_replay_continuation"
	if not os.path.exists(dir_path_output) : os.mkdir(dir_path_output)
	if not os.path.exists(dir_path_video_id) : os.mkdir(dir_path_video_id)
	if not os.path.isdir(dir_path_chat_replay_continuation) : os.makedirs(dir_path_chat_replay_continuation)
	
	first_continuation = get_first_continuation(video_id, ALL_CONTINUATION)
	get_chat_replay_hundler(video_id, first_continuation)
###

####################################################
def run():
	get_youtube_chat_replay()
####################################################
run()