# -*- coding: utf-8 -*-

import os
import youtube_dl
import subprocess

def download_all_file(video_id):
	download_video_with_audio(video_id)
	download_video(video_id)
	download_audio(video_id)
###

dir_path_output = "./output"

def disp_available_youtube_format(video_id) :
	# 取得可能な形式の一覧表示
	cmd = f"youtube-dl https://www.youtube.com/watch?v={video_id} -F"
	subprocess.check_call(cmd, shell=True)
###

def download_video_with_audio(video_id):
	ydl = youtube_dl.YoutubeDL({
		"format":"bestvideo[height=720][vcodec*=avc1][fps=30]+bestaudio/best",
		# "outtmpl":"output/%(id)s/%(id)s_video_and_audio_%(fps)s_%(vcodec)s_%(acodec)s.%(ext)s",
		"outtmpl":f"{dir_path_output}/%(id)s/%(id)s_video_with_audio.%(ext)s",
	})
	with ydl:ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}")
###

def download_video(video_id):
	ydl = youtube_dl.YoutubeDL({
		"format":"bestvideo[height=720][vcodec*=avc1][fps=30]",
		# "outtmpl":"output/%(id)s/%(id)s_only_video_%(fps)s_%(vcodec)s.%(ext)s",
		"outtmpl":f"{dir_path_output}/%(id)s/%(id)s_video.%(ext)s",
	})
	with ydl:ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}")
###

def download_audio(video_id):
	ydl = youtube_dl.YoutubeDL({
		"format":"bestaudio",
		# "outtmpl":f"{ROOT_DIR}/output/%(id)s/%(id)s_audio_%(format)s_%(fps)s_%(acodec)s.%(ext)s",
		"outtmpl":f"{dir_path_output}/%(id)s/%(id)s_audio.%(ext)s",
	})
	with ydl:ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}")
###

####################################################
def run():
	video_id = "34eGN747bw0"
	
	if not os.path.isdir(dir_path_output) : os.makedirs(dir_path_output)

	disp_available_youtube_format(video_id)
	download_video_with_audio(video_id)
	download_video(video_id)
	download_audio(video_id)
####################################################
run()