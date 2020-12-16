やってること
===
seleniumを使ってchromeを使ってgoogleにログインする

ポイント
===
googleを開いて右上のログインボタンからログインしようとすると、  
パスワードを入力してOKボタンを押したタイミングで  
「ロボットお断り」という感じでキックされます。  
なので、真正面からGoogleにログインするのではなく、  
「Google認証するだけのWEBアプリケーション」を自前で用意して、  
それを通過させることでログインした状態にします。  

WEBアプリケーションといっても何かそれらしいものを作るわけではなく、  
実挙動としてはURLを叩いてGoogleログイン画面が表示させるだけです。  
ソースコード読んだらたぶんわかります。  

下準備
===
・Pyothonの開発環境を用意する  
・必要なライブラリをインストールする（ライブラリ管理みたいなことはしてません）  
・Googleアカウントを用意する  
・Google Cloud Platformaで認証情報等をなんやかんやしてCLIENT_IDを用意する  

参考
===
【完全版】PythonとSeleniumでブラウザを自動操作(クローリング／スクレイピング)するチートシート  
https://tanuhack.com/selenium/#Selenium

Gmailアカウントへのサインインが失敗する（セレン自動化）  
https://qastack.jp/programming/59534028/sign-in-to-gmail-account-fails-selenium-automation

Selenium webdriverよく使う操作メソッドまとめ  
https://qiita.com/mochio/items/dc9935ee607895420186

複数のウィンドウを処理する  
https://riptutorial.com/ja/selenium-webdriver/example/29676/%E8%A4%87%E6%95%B0%E3%81%AE%E3%82%A6%E3%82%A3%E3%83%B3%E3%83%89%E3%82%A6%E3%82%92%E5%87%A6%E7%90%86%E3%81%99%E3%82%8B

OAuth 2.0 Flow: Client-side web apps（こっちだとseleniumからログインできない）  
https://developers.google.com/youtube/v3/guides/auth/client-side-web-apps?hl=ja 

OAuth 2.0 Flow: Server-side web apps（こっちだとseleniumからログインできる）  
https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps?hl=ja