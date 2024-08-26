from bot.core import database as db

botdb = db.client["TELEGRAM"]["botcache"]


async def add_bot(data):
  await botdb.insert_one(data)
  return True
async def get_bot(botid):
  return await botdb.find_one( {"userid": int(botid)})


async def approve_bot(botid, verifier):
  k = await botdb.update_one(
      {"userid": int(botid)},
      {"$set": {
          "status": "approved",
          "verified_by": verifier
      }})
  return True

async def publish_bot(botid):
  await botdb.update_one(
      {"userid": int(botid)},
      {"$set": {
          "status": "published"
      }})
  return True

async def reject_bot(botid, verifier):
  await botdb.update_one(
      {"userid": int(botid)},
      {"$set": {
          "status": "rejected",
          "verified_by": verifier
      }})
  return True

async def rate(userID, rating, botID):
       b = await botdb.find_one(
           {"userid": int(botID)})
       await botdb.update_one(
           {"userid": int(botID)},
           {"$set": {
               "ratings": {
                 str(userID) :rating
               },
           }})
       return True