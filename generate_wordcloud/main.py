# -*- coding: utf-8 -*-

import os
import glob
import json
import re
import MeCab
import cv2
from wordcloud import WordCloud, ImageColorGenerator
from urllib.request import urlopen, urlretrieve

RENDERER_TYPE_NONE = ""#指定なし
RENDERER_TYPE_NORMAL = "liveChatTextMessageRenderer"#通常コメント
RENDERER_TYPE_SUPERCHAT = "liveChatPaidMessageRenderer"#スパチャ
RENDERER_TYPE_NEW_MEMBER_OLD = "liveChatLegacyPaidMessageRenderer"#新規メンバー追加（旧？）
RENDERER_TYPE_NEW_MEMBER = "liveChatMembershipItemRenderer"#新規メンバー追加
RENDERER_TYPE_ROWSPEED1 = "liveChatModeChangeMessageRenderer"#低速モード通知1
RENDERER_TYPE_ROWSPEED2 = "liveChatRestrictedParticipationRenderer"#低速モード通知2
RENDERER_TYPE_STICKER = "liveChatPaidStickerRenderer"#ステッカー

def get_file_name_list(dir_path):
	result = []
	file_path_list = sorted(glob.glob(dir_path+"/*"))
	for file_path in file_path_list:
		file_name = os.path.basename(file_path)
		result.append(file_name)
	###
	result.sort()
	
	return result
###

def get_combined_list(videoId, rendererType):
	dir_path = f"../get_youtube_chat_replay/output/{videoId}"
	dir_path_chat_replay_continuation = f"{dir_path}/chat_replay_continuation"
	result = []
	
	file_name_list = get_file_name_list(dir_path_chat_replay_continuation)
	combined_chat_replay_list = []
	for file_name in file_name_list:
		with open(f"{dir_path_chat_replay_continuation}/{file_name}", mode="r", encoding="utf-8_sig") as file:
			if (rendererType == ""):
				result = result + json.loads(file.read())
			else:
				for element in json.loads(file.read()):
					if rendererType == element["renderer_type"]:result.append(element)
				###
			###
		###
	###

	return result
###

def get_tachie_path(channel_id) :
	file_path_tachie_nijisanji = f"./resource/nijisanji/{channel_id}.png" # 背景透過されてる
	file_path_tachie_hololive = f"./resource/hololive/{channel_id}.png" # 背景透過されてる
	file_path_tachie_dummy = f"./resource/hololive/dummy.png" # ダミーの空画像

	if os.path.isfile(file_path_tachie_nijisanji) : return file_path_tachie_nijisanji
	elif os.path.isfile(file_path_tachie_hololive) : return file_path_tachie_hololive
	else : return file_path_tachie_dummy
###

def output_wordcloud_only_image1(channel_id, origin_video_id) :
	# ワードクラウド作成
	dir_path_output = "./output"
	if not os.path.isdir(dir_path_output) : os.mkdir(dir_path_output)
	dir_path_video_id = f"{dir_path_output}/{origin_video_id}"
	if not os.path.isdir(dir_path_video_id) : os.mkdir(dir_path_video_id)
	
	file_path_tachie = get_tachie_path(channel_id)
	print(os.path.isfile(file_path_tachie))
	file_path_wordcloud_only = f"{dir_path_video_id}/{origin_video_id}_wordcloud_only.jpg"
	file_path_font = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"
	
	cl = get_combined_list(origin_video_id, RENDERER_TYPE_NONE)

	text_list = []
	for element in cl : 
		target = element["text"]
		emoji_array = re.findall(r"[[a-zA-Z0-9_]+]", target)
		for emoji in emoji_array : target = target.replace(emoji, "")
		text_list.append(target)
	###
	mcb = MeCab.Tagger("mecabrc")
	res = mcb.parseToNode("".join(text_list))
	output = []
	while res : 
		if res.surface != "" :
			word_type = res.feature.split(",")[0]
			if word_type in ["形容詞", "動詞","名詞", "副詞"] : output.append(res.surface)
		###
		res = res.next
		if res is None : break
	###

	stop_words = [ 'てる', 'いる', 'なる', 'れる', 'する', 'ある',  \
		'こと', 'これ', 'さん', 'して', \
		'くれる', 'やる', 'くださる', 'そう', 'せる', \
		 'した',  '思う',  \
		'それ', 'ここ', 'ちゃん', 'くん', '', \
		'て','に','を','は','の', 'が', 'と', 'た', 'し', 'で', \
		'ない', 'も', 'な', 'い', 'か', 'ので',  \
		'よう', '', 'れ','さ','なっ', '草', '草草', 'こん', '待機',  \
		'こんばんわ', 'こんばんは', "かわいい", "ww"
		]

	img_tachie = cv2.imread(file_path_tachie)
	height_tachie, width_tachie, channels_tachie = img_tachie.shape[:3]
	wc = WordCloud( 
		font_path=file_path_font, 
		background_color="black", 
		# background_color="white", 
		# background_color="#c0c0c0", 
		# background_color="#65ace4", 
		width=width_tachie, 
		height=height_tachie, 
		collocations=False,
		# colormap="prism",
		colormap="Set2",
		stopwords=set(stop_words) 
		).generate(" ".join(output))
	wc.to_file(file_path_wordcloud_only)
###

def output_wordcloud_only_image2(origin_video_id) :
	# ワードクラウド作成
	dir_path_output = "./output"
	if not os.path.isdir(dir_path_output) : os.mkdir(dir_path_output)
	dir_path_video_id = f"{dir_path_output}/{origin_video_id}"
	if not os.path.isdir(dir_path_video_id) : os.mkdir(dir_path_video_id)
	
	file_path_thumbnail_origin = f"./output/{origin_video_id}/{origin_video_id}_thumbnail_origin.jpg"
	file_path_wordcloud_only = f"{dir_path_video_id}/{origin_video_id}_wordcloud_only2.jpg"
	file_path_font = "/System/Library/Fonts/ヒラギノ明朝 ProN.ttc"
	
	cl = get_combined_list(origin_video_id, RENDERER_TYPE_NONE)

	text_list = []
	for element in cl : 
		target = element["text"]
		emoji_array = re.findall(r"[[a-zA-Z0-9_]+]", target)
		for emoji in emoji_array : target = target.replace(emoji, "")
		text_list.append(target)
	###
	mcb = MeCab.Tagger("mecabrc")
	res = mcb.parseToNode("".join(text_list))
	output = []
	while res : 
		if res.surface != "" :
			word_type = res.feature.split(",")[0]
			if word_type in ["形容詞", "動詞","名詞", "副詞"] : output.append(res.surface)
		###
		res = res.next
		if res is None : break
	###

	stop_words = [ 'てる', 'いる', 'なる', 'れる', 'する', 'ある',  \
		'こと', 'これ', 'さん', 'して', \
		'くれる', 'やる', 'くださる', 'そう', 'せる', \
		 'した',  '思う',  \
		'それ', 'ここ', 'ちゃん', 'くん', '', \
		'て','に','を','は','の', 'が', 'と', 'た', 'し', 'で', \
		'ない', 'も', 'な', 'い', 'か', 'ので',  \
		'よう', '', 'れ','さ','なっ', '草', '草草', 'こん', '待機',  \
		'こんばんわ', 'こんばんは', "かわいい", "ww"
		]

	
	img_thumbnail_origin = cv2.imread(file_path_thumbnail_origin)
	height_thumbnail_origin, width_thumbnail_origin, channels_thumbnail_origin = img_thumbnail_origin.shape[:3]
	wc = WordCloud( 
		font_path=file_path_font, 
		background_color="black", 
		# background_color="white", 
		# background_color="#c0c0c0", 
		# background_color="#65ace4", 
		width=width_thumbnail_origin, 
		height=height_thumbnail_origin, 
		collocations=False,
		# colormap="prism",
		colormap="Set2",
		stopwords=set(stop_words) 
		).generate(" ".join(output))
	wc.to_file(file_path_wordcloud_only)
###


def output_wordcloud_combined_image1(channel_id, origin_video_id) :
	# 立ち絵と立ち絵ワードクラウドを合成（透過合成）
	file_path_tachie = get_tachie_path(channel_id)
	file_path_wordcloud_only = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_only.jpg"
	file_path_wordcloud_combined = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_combined1.jpg"

	img_front = cv2.imread(file_path_tachie)
	img_back = cv2.imread(file_path_wordcloud_only)

	alpha = 0.5
	img_wordcloud_combined = cv2.addWeighted(img_front, alpha, img_back, 1 - alpha, 0)
	# cv2.imshow("result", img_wordcloud_combined)
	cv2.imwrite(file_path_wordcloud_combined, img_wordcloud_combined)
###

def output_wordcloud_combined_image2(channel_id, origin_video_id) :
	# 立ち絵と立ち絵ワードクラウドを合成（非透過合成）
	file_path_tachie = get_tachie_path(channel_id)
	file_path_wordcloud_only = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_only.jpg"
	file_path_wordcloud_combined = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_combined2.jpg"

	img_front = cv2.imread(file_path_tachie)
	img_back = cv2.imread(file_path_wordcloud_only)
	
	rows, cols, channels = img_front.shape
	roi = img_back[0:rows, 0:cols]
	
	# Now create a mask of logo and create its inverse mask also
	img_front_gray = cv2.cvtColor(img_front,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img_front_gray, 10, 255, cv2.THRESH_BINARY)
	mask_inv = cv2.bitwise_not(mask)
	
	# Now black-out the area of logo in ROI
	img_back_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
	
	# Take only region of logo from logo image.
	img_front_fg = cv2.bitwise_and(img_front,img_front,mask = mask)
	
	# Put logo in ROI and modify the main image
	dst = cv2.add(img_back_bg, img_front_fg)
	img_back[0:rows, 0:cols ] = dst # change the coordinate #ORI 0:rows, 0:cols 
	# cv2.imshow('res',img_back)
	cv2.imwrite(file_path_wordcloud_combined, img_back)
###

def output_wordcloud_combined_image3(origin_video_id) :
	# 素のワードクラウドとサムネイルを合成（透過合成）
	file_path_thumbnail_origin = f"./output/{origin_video_id}/{origin_video_id}_thumbnail_origin.jpg"
	file_path_wordcloud_only2 = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_only2.jpg"
	file_path_wordcloud_combined3 = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_combined3.jpg"

	img_front = cv2.imread(file_path_wordcloud_only2)
	img_back = cv2.imread(file_path_thumbnail_origin)

	alpha = 0.2
	img_wordcloud_combined = cv2.addWeighted(img_front, alpha, img_back, 1 - alpha, 0)
	cv2.imwrite(file_path_wordcloud_combined3, img_wordcloud_combined)
###


def output_thumbnail_combined_image(origin_video_id, only_wordcloud=False) :
	# 合成後ワードクラウドとサムネイルを合成
	file_path_thumbnail_origin = f"./output/{origin_video_id}/{origin_video_id}_thumbnail_origin.jpg"
	file_path_thumbnail_combined = f"./output/{origin_video_id}/{origin_video_id}_thumbnail_combined.jpg"
	file_path_wordcloud = ""
	if only_wordcloud : file_path_wordcloud = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_only.jpg"
	else : file_path_wordcloud = f"./output/{origin_video_id}/{origin_video_id}_wordcloud_combined2.jpg"
		
	img_thumbnail_origin = cv2.imread(file_path_thumbnail_origin)
	img_wordcloud = cv2.imread(file_path_wordcloud)

	scale = 720 / img_wordcloud.shape[0]
	img_wordcloud = cv2.resize(img_wordcloud, dsize=None, fx=scale, fy=scale)

	x_offset=0
	y_offset=0
	img_thumbnail_origin[y_offset:y_offset+img_wordcloud.shape[0], x_offset:x_offset+img_wordcloud.shape[1]] = img_wordcloud
	cv2.imwrite(file_path_thumbnail_combined, img_thumbnail_origin)
###

def download_origin_thumbnail(origin_video_id) :
	# 元動画のサムネイル取得
	url_thumbnail_origin = f"https://img.youtube.com/vi/{origin_video_id}/maxresdefault.jpg"
	url_thumbnail_origin2 = f"https://img.youtube.com/vi/{origin_video_id}/sddefault.jpg"
	file_path_thumbnail_origin = f"./output/{origin_video_id}/{origin_video_id}_thumbnail_origin.jpg"
	if not os.path.isfile(file_path_thumbnail_origin) :
		try :
			print(url_thumbnail_origin)
			print(file_path_thumbnail_origin)
			urlretrieve(url_thumbnail_origin,"{0}".format(file_path_thumbnail_origin))
		except Exception as e :
			try :
				urlretrieve(url_thumbnail_origin2,"{0}".format(file_path_thumbnail_origin))
			except Exception as e :
				raise e
			###
		###
	###
###

####################################################
def run():
	channel_id = "UC0g1AE0DOjBYnLhkgoRWN1w"
	video_id = "tM4I4_ZvYCE"
	
	dir_path_output = "./output"
	if not os.path.isdir(dir_path_output) : os.makedirs(dir_path_output)
	dir_path_video_id = f"{dir_path_output}/{video_id}"
	if not os.path.isdir(dir_path_video_id) : os.makedirs(dir_path_video_id)
	
	download_origin_thumbnail(video_id) # 元動画のサムネイル取得
# 	output_wordcloud_only_image1(channel_id, video_id) # ワードクラウド作成（立ち絵サイズ）
	output_wordcloud_only_image2(video_id) # ワードクラウド作成（サムネイルサイズ）
# 	output_wordcloud_combined_image1(channel_id, video_id) # 立ち絵と立ち絵ワードクラウドを合成（透過合成）
# 	output_wordcloud_combined_image2(channel_id, video_id) # 立ち絵と立ち絵ワードクラウドを合成（非透過合成）
	output_wordcloud_combined_image3(video_id) # 素のワードクラウドとサムネイルを合成（透過合成）
# 	output_thumbnail_combined_image(video_id) # 合成後ワードクラウドとサムネイルを合成
	
####################################################
run()