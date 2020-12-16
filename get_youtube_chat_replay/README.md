概要
===
youtubeのライブ配信のチャットリプレイを取得するサンプル 　

やってること
===
1. youtubeの動画のページからcontinuationを取得  
2. continuationをパラメータに渡してURLを叩いてチャット取得  
3. チャットの中に次のcontinuationが含まれているので、同様にURLを叩いて以下ループ  

おしまい  

注意点
===
youtube側のJSONの構造は結構コロコロ変わるので、うまく動かなかったら適当にいじりましょうね 　

参考
===
Python3 では、BeautifulSoup3 を pip install できない  
https://www.monotalk.xyz/blog/python3-%E3%81%A7%E3%81%AFbeautifulsoup3-%E3%82%92-pip-install-%E3%81%A7%E3%81%8D%E3%81%AA%E3%81%84/

