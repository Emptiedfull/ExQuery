from main import client
import discord
import json
from ai import get_chat_response, start_chat_sesson


async def read_all(channel,limit=200):
    guild = discord.utils.get(client.guilds, name="test")
    channel = discord.utils.get(guild.channels, name=channel.lower())
    messages = channel.history(limit = limit)
    messages = []
    async for message in channel.history(limit=limit):
        if message.author == client.user:   
             messages.append(message)
    
    messages.reverse()
    return messages

async def send_query(channel,message,user,chat_session,ai = False):
   
    guild = discord.utils.get(client.guilds, name="test")
    channel = discord.utils.get(guild.channels, name=channel.lower())

    res = {
        "Event":"message",
        "Type":"query",
        "User":user,
        "Message":message
    }

    res_json = json.dumps(res)

    if channel:
        await channel.send(f"```json\n{res_json}\n```")
        if ai:
          
            response = get_chat_response(chat_session,message)
            res = {
                "Event":"message",
                "Type":"response",
                "User":"AI",
                "Message":response
            }
            res_json = json.dumps(res)
            await channel.send(f"```json\n{res_json}\n```")
    else:
        print("Channel not found")
        return False
    return True


@client.event
async def on_ready():

    print("Bot Online")

@client.event
async def on_message(message):
    from socketHandler import manager


    if "support" in [role.name for role in message.author.roles]:
        Body = {
            "Event":"message",
            "Type":"query",
            "User":message.author.name + "@Support" ,
            "Message":message.content
        }

        BodyJson = json.dumps(Body)

        await message.channel.send("```json\n"+BodyJson+"\n```")

       
    
    
    BodyJson = message.content[7:-3]
    Body = json.loads(BodyJson)

    Body["Event"] = "message"
    BodyJson = json.dumps(Body)
    
    for client in manager.chatrooms.get(message.channel.name.upper(), []):

         await client["websocket"].send_text(BodyJson)


