import math
from bot.core.utils import generate_keyboard
class BotPreview:
  def __init__(self):
      self.id = None
      self.title = None
      self.username = None
      self.pic = None
      self.description = None
      self.rating = 0
      self.votes = 0
      self.developer = None
      self.category = None
      self.language = "English"
      self.inline_support = "no"
      self.group_support = "no"
      self.tags = None
  def get_caption(self):
      caption = f'''
<b>{self.title}</b>
<blockquote expandable>{self.description}</blockquote>
➖➖➖
<b>Username:</b> @{self.username}
<b>Rating:</b> {'⭐️'* math.floor(self.rating)} <i>({self.rating}/5 on {self.votes} votes)</i>
➖➖➖
🧑‍💻 <b>Developer:</b> <i>{self.developer}</i>
🗂 <b>Category:</b> <i>{self.category}</i>
🌐 <b>Languages:</b> <i>{self.language}</i>
💬 <b>Inline:</b> <i>{self.inline_support}</i>
👥 <b>Groups:</b> <i>{self.group_support}</i>

#️⃣ <b>Tags:</b> <i>{self.tags}</i>
          '''
      return caption
  def get_keyboard(self):
      btn = f'''
      [Edit Title {'✅' if self.title else '❌'}](data::ed_title) [Edit Botpic {'✅' if self.pic else '❌'}](data::ed_pic)
      [Edit Description {'✅' if self.description else '❌'}](data::ed_description) [Edit Language {'✅' if self.language else '❌'}](data::ed_language)
      [Edit Category {'✅' if self.category else '❌'}](data::ed_category) [Edit Tags {'✅' if self.tags else '❌'}](data::ed_tags)

      [SUBMIT](data::submit)
              '''
      return generate_keyboard(btn)
  def ready(self):
      return self.title and self.username and self.pic and self.description and  self.category and  self.language and self.inline_support and  self.group_support and  self.tags
