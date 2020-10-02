from graph import make_graph, make_sorted_graph
from discord.ext import tasks
import discord
import json
import datetime
from scrape import get_html_from_labpage, get_num_lab_dict, get_str_numjson_diff, dict2jsonfile


def getMessage():
    page_source = get_html_from_labpage()
    num_lab_dict = get_num_lab_dict(page_source)
    sorted_num_lab_list = sorted(
        num_lab_dict.items(), key=lambda x: x[1], reverse=True)
    make_graph(num_lab_dict, "figure.png")
    make_sorted_graph(sorted_num_lab_list, "sorted.png")

    before_num_lab_dict = {}
    with open('num_lab.json') as file:
        before_num_lab_dict = json.load(file)

    ret_str = get_str_numjson_diff(before_num_lab_dict, num_lab_dict)
    dict2jsonfile(num_lab_dict, 'num_lab.json')

    return ret_str


config_dict = {}
with open('config.json') as file:
    config_dict = json.load(file)

TOKEN = config_dict["DISCORD_TOKEN"]
DISCORD_CHANNEL_ID = config_dict["DISCORD_CHANNEL_ID"]

client = discord.Client()

channel_sent = None


@tasks.loop(seconds=120)
async def send_message_every_10sec():
    message = getMessage()
    print(message, str(datetime.datetime.now()))
    if message != "希望人数に差異はありませんでした":
        await channel_sent.send(message)


@client.event
async def on_ready():
    global channel_sent
    channel_sent = client.get_channel(DISCORD_CHANNEL_ID)
    # await channel_sent.send("botが起動しました")
    send_message_every_10sec.start()


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/graph':
        await channel_sent.send('各研究室の希望人数をグラフで表示します', file=discord.File('figure.png'))
    elif message.content == '/sorted':
        await channel_sent.send('各研究室の希望人数をソートしてグラフで表示します', file=discord.File('sorted.png'))

client.run(TOKEN)
