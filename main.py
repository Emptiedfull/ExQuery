from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import discord
from contextlib import asynccontextmanager
import asyncio
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

DB_uri = os.getenv("DB_URI")
discord_token = os.getenv("DISCORD_TOKEN")

@asynccontextmanager
async def lifespan(app: FastAPI):
    import bot
    asyncio.create_task(client.start(discord_token))
    from apiHandlers.auth import router as auth_router
    from apiHandlers.channels import router as channel_router
    from socketHandler import websocket_router

   
    
    app.include_router(auth_router)
    app.include_router(channel_router)
    app.include_router(websocket_router)


    @app.get("/{path:path}")
    async def serve(path: str):
        return FileResponse("build/index.html")
    yield
    dbclient.close()
    await client.close()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="build/static"), name="static")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
dbclient = pymongo.MongoClient(DB_uri)
print("DB Online")







