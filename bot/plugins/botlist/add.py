import math
import os
import tempfile
from pyrogram.errors import UsernameInvalid

from pyrogram import Client, filters
from pyrogram.enums import ListenerTypes
from pyrogram.types import InputMediaPhoto
from bot.core import database as db
from bot.core import filters as fltr
from bot.core.utils import generate_keyboard

from .resize import extend_uniform_background


@Client.on_message(filters.command(["add", "new"]))
async def addTheBot(client, message):
    warn = f'''
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
        return await fetch_msg.edit("❌ Username invalid")
    if not chat.is_bot:
       return await message.reply("This is not a bot.")

    cap = '''
<b>{title}</b>
<blockquote expandable>{description}</blockquote>
➖➖➖
<b>Username:</b> @{username}
<b>Rating:</b> {stars} <i>({rating}/5 on {votes} votes)</i>
➖➖➖
🧑‍💻 <b>Developer:</b> <i>{developer}</i>
🗂 <b>Category:</b> <i>{category}</i>
🌐 <b>Languages:</b> <i>{language}</i>
💬 <b>Inline:</b> <i>{inline_support}</i>
👥 <b>Groups:</b> <i>{group_support}</i>

#️⃣ <b>Tags:</b> <i>{tags}</i>
    '''

    title = chat.first_name
    description = None
    username = chat.username
    rating = 0
    stars = '⭐️'* math.floor(rating)
    votes = 0
    developer = None
    category = None
    language = "English"
    inline_support = "no"
    group_support = "no"
    tags = None
    
    btn = '''
[Edit Title](data::ed_title) [Edit Botpic](data::ed_pic)
[Edit Description](data::ed_description) [Edit Language](data::ed_language)
[Edit Category](data::ed_category) [Edit Tags](data::ed_tags)

[SUBMIT](data::submit)
        '''
    keyboard = generate_keyboard(btn)
    
    caption = cap.format(title=title, description=description, username=username, stars=stars,rating=rating, votes=votes, developer=developer, category=category, language=language, inline_support=inline_support, group_support=group_support,tags=tags)

    with tempfile.TemporaryDirectory(prefix=f"{message.from_user.id}_") as temp_dir:
        temp_file_path = os.path.join(temp_dir, 'original.jpg')
        temp_out_file = os.path.join(temp_dir, 'output.jpg')
        await client.download_media(chat.photo.big_file_id, file_name = temp_file_path)

        extend_uniform_background(temp_file_path, 2560, 1440, temp_out_file)
        await fetch_msg.delete()
        post = await message.reply_photo(photo=temp_out_file,caption=caption,reply_markup=keyboard)
    flow = True
    while flow:
        media = None
        
        ask = await client.listen(message_id = post.id,listener_type =ListenerTypes.CALLBACK_QUERY)
        await ask.answer()
        if ask.data == "submit":
            flow = False
            await client.send_photo("thebotslist", photo=post.photo.file_id,caption=cap.format(title=title, description=description, username=username, stars=stars, rating=rating, votes=votes, developer=developer, category=category, language=language, inline_support=inline_support, group_support=group_support,tags=tags),reply_markup=generate_keyboard("[1⭐️](data::st_1) [2⭐️](data::st_2) [3⭐️](data::st_3)\n[4⭐️](data::st_4) [5⭐️](data::st_5)"))
            await ask.reply("submited successfully")
        if ask.data == "ed_title":
            ask_it = await message.chat.ask("Enter the title")
            title = ask_it.text
        if ask.data == "ed_pic":
            ask_it = await message.chat.ask("Send me the picture")
            if ask_it.photo:
                media = ask_it.photo.file_id
            else:
                await ask_it.reply("Send me as picture")
        if ask.data == "ed_description":
            ask_it = await message.chat.ask("Enter the description\n\nmin 50 max 300 characters")
            description = ask_it.text
            
        if ask.data == "ed_language":
            ask_it = await message.chat.ask("Enter the language")
            language = ask_it.text
        
        if ask.data == "ed_category":
             ask_it = await message.chat.ask("Select the category")
             category = ask_it.text
        
        if ask.data == "ed_tags":
             ask_it = await message.chat.ask("Enter the tags")
             tags = ask_it.text
        await ask_it.sent_message.delete()
        new_caption = cap.format(title=title, description=description, username=username, stars=stars, rating=rating, votes=votes, developer=developer, category=category, language=language, inline_support=inline_support, group_support=group_support,tags=tags)
        if media:
            await post.edit_media(media=InputMediaPhoto(media, caption = new_caption),reply_markup=keyboard)
        else:
            await post.edit_caption(caption = new_caption ,reply_markup=keyboard)
        
   
   
           
async def verified(client, message):
           caption = "**RingtoneRobot**\n<blockquote expandable>This bot can add view counters to messages, get user, channel, group and sticker IDs, upload text and images to Telegraph and remove many system messages in groups.</blockquote>\n➖➖➖\n**Username:** @RingtoneRobot\n**Rating:** ⭐️⭐️⭐️⭐️ (4.3/5 on 130 votes)\n➖➖➖\n🧑‍💻 **Developer:** Quantum\n🗂 **Category:** Music\n🌐 **Languages:** English\n💬 **Inline:** no\n👥 **Groups:** yes\n\n#️⃣ **Tags:** #ringtone #download #song #music #ringtonerobot"
           btn = "[1⭐️](data::rt_1) [2⭐️](data::rt_2) [3⭐️](data::rt_3)\n[4⭐️](data::rt_4) [5⭐️](data::rt_5)"
           keyboard = generate_keyboard(btn)
           await message.reply_photo(
               photo=
               "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTjtbd1HYppJ-yyGqbeB4GoQWEjDa2ADpoVg&s",
               caption=caption,reply_markup=keyboard)
