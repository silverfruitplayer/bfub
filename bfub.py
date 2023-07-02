from pyrogram import Client, filters
from config import bot_token, sudo_chats_id
import wget
import requests
import os
import time
import re
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

app = Client(":memory:", bot_token=bot_token, api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

DOWNLOAD = "./"
api_key = '261187gz7nyenfkfk6ttgx'

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
    api_url = 'https://api.doodapi.com/v1/files/upload'
    file_path = ''
    headers = {
        'Authorization': api_key
    }
    
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
        await m.edit("Uploading Now to doodstream....")
        r = requests.post(api_url, headers=headers, files=files)
        text = r.json()
        if r.ok:
            file_id = text['file_id']
            file_url = text['file_url']
            x = f"""
            Upload successful To DoodStream.\n**File ID:** {file_id}\n**File URL:** {file_url}"
            """
            await m.reply(x)
            os.remove(file_path)
        else:
            return await m.edit("Failed.")
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
        r = requests.post("api.anonfiles.com/upload", files=files)
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
