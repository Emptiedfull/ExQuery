from fastapi import FastAPI,WebSocket,WebSocketDisconnect,Header,Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRouter
from utils import get_user,validateChannel
import bot,json
from ai import start_chat_sesson,get_chat_response

websocket_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.chatrooms = {}
        self.chatSessions = {}

    async def connect(self,websocket: WebSocket,room: str,user: str):
      
        if room in self.chatrooms.keys():
            
            self.chatrooms[room].append({"user": user, "websocket": websocket})
        else:
            print("Creating chat session")
 
            self.chatSessions[room] = start_chat_sesson()
            self.chatrooms[room] = [{"user": user, "websocket": websocket}]
        print(f'Connected to {room} by {user}')
        await websocket.accept()
        messages = await bot.read_all(room)
        for message in messages:
            await websocket.send_text(message.content[7:-3])
        
        
    
manager = ConnectionManager()


@websocket_router.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket,token:str = Query(None)):
    room = websocket.path_params["room"]
 
    
    if token is None:
        print("Authorization header not found")
        await websocket.close(code=1008)
        return
   
    userAuth = get_user(token)
    if not userAuth:
        print("Invalid token")
        await websocket.close(code=1008)
        return
    user = userAuth.get("username")
    
    if not validateChannel(room,userAuth.get("email")):
        print("Invalid channel")
        await websocket.close(code=1008)
        return

   

    await manager.connect(websocket,room,user)
    try:
        while True:
            data = await websocket.receive_text()
            await Handle_Socket(data,manager,room,user,websocket,manager.chatSessions[room])
    except WebSocketDisconnect:
        manager.chatrooms[room] = [client for client in manager.chatrooms[room] if client["websocket"] != websocket]
        print(f'Disconnected from {room} by {user}')



async def Handle_Socket(message,manager,room,user,websocket,chat_session):

    try:
        Body = json.loads(message)

        if Body.get("Request_type") == "query":
            await bot.send_query(room,Body.get("Message"),user,chat_session,Body.get("Ai"))


    except Exception as e:
        print(e)
        return
   


    
