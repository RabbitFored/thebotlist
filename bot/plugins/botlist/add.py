import math
import os
import tempfile
from pyrogram.errors import UsernameInvalid
import datetime

from pyrogram import Client, filters
from pyrogram.enums import ListenerTypes
from pyrogram.types import InputMediaPhoto
from bot.core import database as db
from .db import add_bot
from bot.core import filters as fltr
from bot.core.utils import generate_keyboard
from bot import logger
from .resize import extend_uniform_background
from .preview import BotPreview



@Client.on_message(filters.command(["add", "new"]))
async def addTheBot(client, message):

    warn = '''
**Before sumbitting the bot, make sure that your bot follows these rules:**
1) It should not contain any 18+ or other illegal contents.
2) Bots made with tools like manybots, livegram are not allowed.
3) No cloned bots should be submitted
4) Bots which promote illegal activities are not allowed

__Now send the username of the bot you want to suggest__
'''
    botid = await message.chat.ask(warn, reply_to_message_id = message.id)
    fetch_msg = await botid.reply_text("Fetching info...", quote = True)
    try:
        chat = await client.get_users(botid.text)
    except UsernameInvalid:
        return await fetch_msg.edit("❌ Username invalid.\n\nSend your bot's username in the format: @mailableBot")
    if not chat.is_bot:
       return await message.reply("This is not a bot.")

   
    Preview = BotPreview()
    Preview.id = chat.id
    Preview.title = chat.first_name
    Preview.username = chat.username
    Preview.pic = chat.photo.big_file_id if chat.photo else None

    with tempfile.TemporaryDirectory(prefix=f"{message.from_user.id}_") as temp_dir:
        if chat.photo:
          temp_file_path = os.path.join(temp_dir, 'original.jpg')
          temp_out_file = os.path.join(temp_dir, 'output.jpg')
        
          await client.download_media(chat.photo.big_file_id, file_name = temp_file_path)
          extend_uniform_background(temp_file_path, 2560, 1440, temp_out_file)
          await fetch_msg.delete()

          photo_path = temp_out_file
        else:
            photo_path = "public/assets/default_pic.jpg"

        
        post = await message.reply_photo(photo=photo_path,caption=Preview.get_caption(),reply_markup= Preview.get_keyboard())
    while True:
      try:
        media = None
        ask = await client.listen(message_id = post.id,listener_type =ListenerTypes.CALLBACK_QUERY)
        await ask.answer()
        if ask.data == "submit":
            if Preview.ready():
              data = {
                  "userid" : chat.id,
                  "name": chat.first_name,
                  "username": chat.username,
                  "dc": chat.dc_id if chat.dc_id else 0,
                  "preview_img": post.photo.file_id,
                  "submitted_by": ask.from_user.id,
                  "submitted_on": datetime.datetime.now(),
                  "info": {
                      "description": Preview.description,
                      #developer = b['developer']
                      "category": Preview.category,
                      "language" : Preview.language,
                      "inline_support" : Preview.inline_support,
                      "group_support" : Preview.group_support,
                      "tags" : Preview.tags
                  }
              }
              await add_bot(data)
              await client.send_photo(-1002233681213, photo=post.photo.file_id,caption=Preview.get_caption(),reply_markup=generate_keyboard(f"[Approve ✅](data::approve_{Preview.id}_{ask.from_user.id})\n[Reject ❌](data::reject_{Preview.id}_{ask.from_user.id})") , reply_to_message_id =32016)
              return await ask.message.reply("submited successfully")
            else:
                 await message.reply("❌ Fill all fields to subit bot")
        if ask.data == "ed_title":
            ask_it = await message.chat.ask("Enter the title")
            Preview.title = ask_it.text
        if ask.data == "ed_pic":
            ask_it = await message.chat.ask("Send me the picture")
            if ask_it.photo:
                Preview.media = ask_it.photo.file_id
            else:
                await ask_it.reply("Send me as picture")
        if ask.data == "ed_description":
            ask_it = await message.chat.ask("Enter the description\n\nmin 50 max 300 characters")
            Preview.description = ask_it.text
            
        if ask.data == "ed_language":
            ask_it = await message.chat.ask("Enter the language")
            Preview.language = ask_it.text
        
        if ask.data == "ed_category":
              ask_it = await message.chat.ask("Select the category")
              Preview.category = ask_it.text
        
        if ask.data == "ed_tags":
             ask_it = await message.chat.ask("Enter the tags")
             Preview.tags = ask_it.text
        await ask_it.sent_message.delete()
        if media:
            await post.edit_media(media=InputMediaPhoto(media, caption=Preview.get_caption()),reply_markup= Preview.get_keyboard())
        else:
            await post.edit_caption(caption=Preview.get_caption(),reply_markup= Preview.get_keyboard())
      except Exception as e:
          logger.info(f"{e}")
   
   
           
async def verified(client, message):
           caption = "**RingtoneRobot**\n<blockquote expandable>This bot can add view counters to messages, get user, channel, group and sticker IDs, upload text and images to Telegraph and remove many system messages in groups.</blockquote>\n➖➖➖\n**Username:** @RingtoneRobot\n**Rating:** ⭐️⭐️⭐️⭐️ (4.3/5 on 130 votes)\n➖➖➖\n🧑‍💻 **Developer:** Quantum\n🗂 **Category:** Music\n🌐 **Languages:** English\n💬 **Inline:** no\n👥 **Groups:** yes\n\n#️⃣ **Tags:** #ringtone #download #song #music #ringtonerobot"
           btn = "[1⭐️](data::rt_1) [2⭐️](data::rt_2) [3⭐️](data::rt_3)\n[4⭐️](data::rt_4) [5⭐️](data::rt_5)"
           keyboard = generate_keyboard(btn)
           await message.reply_photo(
               photo=
               "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTjtbd1HYppJ-yyGqbeB4GoQWEjDa2ADpoVg&s",
               caption=caption,reply_markup=keyboard)
