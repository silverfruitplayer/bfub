from pyrogram import Client, filters
from config import bot_token, sudo_chats_id
import wget
import requests
import os
import time
import speedtest
import re
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

app = Client(":memory:", bot_token=bot_token, api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

DOWNLOAD = "./"


@app.on_message(filters.command("start") & filters.chat(sudo_chats_id))
async def start(_, message):
    await message.reply_text("Use /help kthxbye")

@app.on_message(filters.command("help"))
async def help(_, message):
    txt = """/url [url] - Upload Files Via URL
/tg - Upload Files Via Telegram"""
    await message.reply_text(txt)

@app.on_message(filters.command("url"))
async def url(_, message):
    if len(message.command) != 2:
        await message.reply_text("/url [url]")
        return
    if message.entities[1]['type'] != "url":
        await message.reply_text("/url [url]")
        return
    m = await message.reply_text("downloading....bot will be unresponsive until download finishes.")
    lenk = message.text.split(None, 1)[1]
    try:
        filename = wget.download(lenk)        
        files = { 'file': open(filename, 'rb')}
        await m.edit("Uploading....")
        r = requests.post("https://api.bayfiles.com/upload", files=files)
        text = r.json()
        output = f"""
**status:** `{text['status']}`
**link:** {text['data']['file']['url']['full']}
**id:** `{text['data']['file']['metadata']['id']}`
**name:** `{text['data']['file']['metadata']['name']}`
**size:** `{text['data']['file']['metadata']['size']['readable']}`"""
        await message.reply_text(output)
        os.remove(filename)
    except Exception as e:
        print(str(e))
        await m.edit(str(e))
        return

def convert(speed):
    return round(int(speed) / 1048576, 2)

@app.on_message(filters.command("speedtest"))
async def speedtestxyz(client, message):
    buttons = [[InlineKeyboardButton("Image",
                                    callback_data="speedtest_image"),
                InlineKeyboardButton("Text",
                                    callback_data="speedtest_text")]]
    await message.reply_text(
        "Select SpeedTest Mode",
        reply_markup=InlineKeyboardMarkup(buttons))


def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def speedtest_callback(_, __, query):
    if re.match("speedtest", query.data):
        return True


speedtest_create = filters.create(speedtest_callback)


@app.on_callback_query(speedtest_create)
async def speedtestxyz_callback(client, query):
        await query.message.edit_text('Runing a speedtest....')
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = 'SpeedTest Results:'

        if query.data == 'speedtest_image':
            speedtest_image = speed.results.share()
            replym = f"[SpeedTest Results:]({speedtest_image})"
            await query.message.edit_text(replym, parse_mode="markdown")

        elif query.data == 'speedtest_text':
            result = speed.results.dict()
            replymsg += f"\n - **ISP: {result['client']['isp']}"
            replymsg += f"\n - Download: {speed_convert(result['download'])}"
            replymsg += f"\n - Upload: {speed_convert(result['upload'])}"
            replymsg += f"\n - Ping: {result['ping']}"
            await query.message.edit_text(replymsg, parse_mode="markdown")    
   

@app.on_message(filters.command("bay") & filters.chat(sudo_chats_id))
async def tg(_, message):
    now = time.time()
    if not message.reply_to_message:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    if not message.reply_to_message.media:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    m = await message.reply_text("Downloading Document.")
    file_path = await message.reply_to_message.download(DOWNLOAD)
    try:
        files = { 'file': open(file_path, 'rb')}
        await m.edit("Uploading....")
        r = requests.post("https://api.bayfiles.com/upload", files=files)
        text = r.json()
        output = f"""
**status:** `{text['status']}`
**link:** {text['data']['file']['url']['full']}
**id:** `{text['data']['file']['metadata']['id']}`
**name:** `{text['data']['file']['metadata']['name']}`
**size:** `{text['data']['file']['metadata']['size']['readable']}`"""
        await message.reply_text(output)
        os.remove(file_path)      
    except Exception as e:
        print(str(e))
        await m.edit(str(e))
        return
@app.on_message(filters.command("anon") & filters.chat(sudo_chats_id))
async def tg(_, message):
    file_path = ''
    if not message.reply_to_message:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    if not message.reply_to_message.media:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    m = await message.reply_text("Downloading Document.")
    file_path = await message.reply_to_message.download()
    try:
        files = { 'file': open(file_path, 'rb')}
        await m.edit("Uploading....")
        r = requests.post("https://api.anonfiles.com/upload", files=files)
        text = r.json()
        output = f"""
**status:** `{text['status']}`
**link:** {text['data']['file']['url']['full']}
**id:** `{text['data']['file']['metadata']['id']}`
**name:** `{text['data']['file']['metadata']['name']}`
**size:** `{text['data']['file']['metadata']['size']['readable']}`"""
        await message.reply_text(output)
        os.remove(file_path)      
    except Exception as e:
        print(str(e))
        await m.edit(str(e))
        return
app.run()
