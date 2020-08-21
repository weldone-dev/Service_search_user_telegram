from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from quart import Quart
from hypercorn.config import Config
import hypercorn.asyncio
import re
from database import *
# get api_id and api_hash https://my.telegram.org/auth
api_id = 0
api_hash = ""   

app = Quart(__name__)
client = TelegramClient("name", api_id, api_hash)

@app.before_serving
async def startup():
    await client.connect()
@app.after_serving
async def cleanup():
    await client.disconnect()

@app.route('/telegram/<userid>', methods=["GET"])
async def searth_userid(userid):
    searth = get_userid(userid)
    if get_userid(userid):
        print(searth)
        return f"{searth}"
    else:
        return "NULL"
@app.route('/telegram/@<username>', methods=["GET"])
async def searth_username(username):
    if not(username) or not(username == re.sub(r'[^A-z0-9_]', "", username)):
        return "NULL"
    try:
        searth = await client(GetFullUserRequest(
            id="@"+username
        ))
        searth = searth.user.id
        print(searth)
        return str(searth)
    except Exception as e:
        print(e)
        return "NULL"
    

    
async def main():
    config = Config()
    config.bind = ["localhost:8080"] 
    await hypercorn.asyncio.serve(app, config)
if __name__ == '__main__':
    client.loop.run_until_complete(main())
   