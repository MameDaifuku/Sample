概要
===
Twitter APIを使ってツイートしたりリプライしたりする  

大筋としては  
①ツイッターアカウントを作成  
②そのアカウントを使ってTwitter Developer Platformにログイン  
③Twitter Developer Platformでアプケーション登録をしてトークン等を生成  
④そのトークン等を使って認証通してAPIをコール  
＞①で作成したツイッターアカウントからツイートしたりDM送信したりする  

注意
===
リプライやDMを送る先のツイッターアカウントをあらかじめ用意しておきましょう。  

Twitter Developersでアプリケーションのpermissionを変更したらAccess Tokenを再生成しないといけないっぽい。  
（アプリの状態とトークンが紐づいている？）  

参考
===
Twitter Developer Platform  
https://developer.twitter.com/ja

PythonでTwitter API を利用していろいろ遊んでみる  
https://qiita.com/bakira/items/00743d10ec42993f85eb

Twitter 開発者 ドキュメント日本語訳  
http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/Rate-Limits-Chart.cgi

Twitter（ツイッター）の検索コマンド全22選　日付やアカウントを指定して探す  
https://mag.app-liv.jp/archive/81735/#410762

POST statuses/update - ツイートを投稿する  
https://syncer.jp/Web/API/Twitter/REST_API/POST/statuses/update/

Twitterの古いダイレクトメッセージAPIは2018年6月に廃止らしい  
https://blog.fkoji.com/2018/02152302.html

Sending and receiving events  
https://developer.twitter.com/en/docs/twitter-api/v1/direct-messages/sending-and-receiving/api-reference/new-event

【Python】TwitterのAPIを使ってダイレクトメッセージを送る  
https://tadaken3.hatenablog.jp/entry/python-sent-dm

TwitterのDM botをpollingベースで作ってみる（TwythonやめてRequestsでAPI直叩きにしてみた）  
https://qiita.com/y_uehara1011/items/22c680ea0e0b13c7942b

Pythonでtwitter APIからRT、リプライ、画像付きツイートを除外してツイートを取得したい  
https://teratail.com/questions/256341
