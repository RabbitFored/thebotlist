from pyrogram import Client
from bot.core import filters as fltr
import importlib
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from bot import strings, ProcessManager 
from bot.core import utils
from pyrogram import enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_callback_query(fltr.on_marker("st"))
async def rate_bot(client, query):
    userid = query.from_user.id
    chatid = query.message.chat.id
    c = -1001475798954
    messageId = query.message.id
    data = query.data
    rating = data.split("_")[1]
  
    try:
      await client.get_chat_member(chatid, userid)
    except UserNotParticipant:
      return await query.answer("❌ Join the channel to vote this bot", show_alert =True )
    except ChatAdminRequired:
      logger.error("Chat Admin Permission Required to perform this function")
      return
    await query.answer(f"You rated: {rating}")
    print(userid,chatid,messageId,rating)