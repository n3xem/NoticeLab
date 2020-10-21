# NoticeLab
This is a daemon script that graphs the number of people who want to join each lab at the university and posts it to the discord app.(Not currently available.)  
大学の各研究室に入りたい人の数をグラフにして、discordアプリに投稿するデーモンスクリプトです。（現在、研究室の募集期間が終わったため使用できません）

# Requirement
Python 3.7.7

# Install
```
touch config.json
```
で、設定ファイルを作り、設定ファイルの中身を
```
{
    "ID": ここにID,
    "PW": ここにPW,
    "DISCORD_CHANNEL_ID": DiscordのチャンネルID,
    "DISCORD_TOKEN": Discordアプリのトークン,
    "OS": 使用しているOS(Windows10なら"Windows10")
}
```
とします。次に、
```
$ python -m pip install -r requirements.txt
```
とコマンドを実行し、実行に必要なパッケージを取得します。（必要に応じて、venvなどを利用してください）  
最後に、
```
$ python init.py
```
と実行し、エラーが出なければインストール完了です。  

# Usage
```
$ python bot_run.py
```
でボットを実行状態にします。  
ボットは2分おきに研究室の希望人数を取得しに行き、増減があればdiscordに通知します。  
![増減の通知](https://i.imgur.com/noM05Oq.png)  
また、botが稼働しているサーバーのチャットに「/sorted」とチャットを送ると、config.jsonで設定したDiscordのチャンネルに、ソートされたグラフが表示されます。  
![グラフ](https://i.imgur.com/l0bJMSb.png)
