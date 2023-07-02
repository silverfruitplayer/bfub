from pyrogram import Client, filters, idle
from config import sudo_chats_id
import wget
import requests
import os
import time
import re
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = Client(":memory:", bot_token="6130122799:AAFR_Ubokp3zSCFheVuRT9z0ulvzwvvWdng", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

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

@app.on_message(filters.command("dood") & filters.chat(sudo_chats_id))
async def dood(_, message):    
    if not message.reply_to_message:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    if not message.reply_to_message.media:
        await message.reply_text("Reply To A File With /tg To Upload")
        return
    m = await message.reply_text("Downloading Document.")
    api_url = 'https://dio118p.dood.video/upload/01?261187gz7nyenfkfk6ttgx'
    file_path = ''
    file_path = await message.reply_to_message.download()
    try:
        files = { 'file': open(file_path, 'rb')}
        await m.edit("Uploading Now to doodstream....")
        r = requests.post(api_url, files=files)
        text = r.json()
        if r.ok:
            await m.reply(text)
            os.remove(file_path)
        else:
            return await m.edit("Failed.")
    except Exception as e:
        print(str(e))
        await m.edit(str(e))
        return
        
app.start()
idle()
