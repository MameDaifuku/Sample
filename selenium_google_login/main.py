# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
import urllib.parse

def testSeleniumChrome() :

	# Seleniumをあらゆる環境で起動させるChromeオプション
	options = Options()
	options.add_argument('--disable-gpu');
	options.add_argument('--disable-extensions');
	options.add_argument('--proxy-server="direct://"');
	options.add_argument('--proxy-bypass-list=*');
	options.add_argument('--start-maximized');
	options.add_argument('--disable-web-security');
	options.add_argument('--allow-running-insecure-content');
	# options.add_argument('--headless'); # ※ヘッドレスモードを使用する場合、コメントアウトを外す

	DRIVER_PATH = 'lib/chromedriver'
	# DRIVER_PATH = '/Users/Kenta/Desktop/Selenium/chromedriver' # ローカル
	# DRIVER_PATH = '/app/.chromedriver/bin/chromedriver'        # heroku

	# ブラウザの起動
	driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
	try:
		CLIENT_ID ="[あなたのCLIENT_ID]"
		redilect_url = "https://www.youtube.com" # Google認証を通した後のリダイレクト先。とりあえずyoutubeに飛ばしておきます

		url_oauth = \
			"https://accounts.google.com/o/oauth2/auth" \
			+ "?client_id=" + CLIENT_ID \
			+ "&redirect_uri=" + redilect_url \
			+ "&scope=" + "email profile" \
			+ "&response_type=code" \
			+ "&access_type=offline"
		
		login_id = "[あなたのGoogleのID]"
		login_password = "[あなたのGoogleのパスワード]"

		# TODO sleepでサボってるところは、本当はdomの存在チェックでちゃんと待機するようにしたい	
		
		# 	Googleログイン画面へ遷移（ブラウザは遷移が完了するまで待機してくれる。賢い。）
		driver.get(url_oauth)
		
		# 	ユーザーIDに値をセットして次へ
		driver.find_element_by_xpath("//*[@id='identifierId']").send_keys(login_id)
		driver.find_element_by_xpath("//*[@id='identifierNext']").click()
		time.sleep(5) # 待機を挟まないとちゃんと処理できない。
		
		# パスワードに値をセットして完了。リダイレクト先へリダイレクトされる
		driver.find_element_by_xpath("//*[@id='password']/div[1]/div/div[1]/input").send_keys(login_password)
		driver.find_element_by_xpath("//*[@id='passwordNext']").click()
		time.sleep(5)

		# おまけ
		# ファイル選択ダイアログを開いてファイル指定するようなヤツは、inputに対してファイルパスをsend_keysするといける
		# driver.find_element_by_xpath("//*[@name='Filedata']").send_keys(file_path_video)

		# inputに対して文字列をセットする場合、clearしないと末尾に文字列が追加される
		# title_element = driver.find_element_by_xpath("//*[@aria-label='動画について説明するタイトルを追加しましょう']")
		# title_element.clear()
		# title_element.send_keys("This is Title")
		
		driver.close()
	finally:
		driver.quit()
	###
###

####################################################
def run():
	testSeleniumChrome()
####################################################
run()