from fastapi import FastAPI, HTTPException,APIRouter,Header
from utils import create_token, decode_token,get_user
import dbhandler as dbhandler,discord
from main import dbclient,client
import random,string,asyncio
router = APIRouter()
import json
from ai import start_chat_sesson,get_chat_response

@router.post("/channels/create")
async def create_channel(Authorization: str = Header(None)):
   
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")    
    try:
        name = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
        token = Authorization.split(" ")[1]
        user = get_user(token)
        name = (user.get("username") + "-" + name).upper()
        if user:
            guild = discord.utils.get(client.guilds, name="test")
            channel = discord.utils.get(guild.channels, name=name)
            if not channel:
                category_name = user.get("username")
                category = discord.utils.get(guild.categories, name=category_name)
                if not category:
                    category = await guild.create_category(category_name)
                
                channel = await guild.create_text_channel(name, category=category)
                
                

                res ={
                    "Event":"create",
                    "Type":"channel",
                    "Channel":name

                }

                await channel.send(f"```json\n{json.dumps(res)}\n```")





            return dbhandler.add_channel(dbclient, name, user.get("email"))
        else:
            raise HTTPException(status_code=402, detail="Unauthorized")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail="Unauthorized")

@router.get("/channels/get")
def get_channels(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Unauthorized")    
    try:
        token = Authorization.split(" ")[1]
        user = get_user(token)
        if user:
            channels = dbhandler.get_channels(dbclient, user.get("email"))
            print(channels)
            return {"channels": channels}
        else:
            raise HTTPException(status_code=402, detail="Unauthorized")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail="Unauthorized")
    
