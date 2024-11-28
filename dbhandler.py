def get_users(client):
    db = client["queries"]
    users = db["users"]
    res = list(users.find({}))
    return res

def get_user(client,email):
    print(client, email)
    db = client["Queries"]
    users = db["users"]
    res = users.find_one({"email":email})
    return res

def get_user_by_username(client,username):
    db = client["Queries"]
    users = db["users"]
    res = users.find_one({"username":username})
    return res

def add_user(client,email,password,username):
    print(client, email, password, username)
    db = client["Queries"]
    users = db["users"]
    if get_user(client,email):
        return False
    if get_user_by_username(client,username):
        return False
    
    users.insert_one({"email":email,"password":password,"username":username})
    return True

def add_channel(client,channel_id,email):
    db = client["Queries"]
    channels = db["channels"]
    channel = channels.find_one({"channel_id":channel_id})
    if channel:
        if email not in channel.get("emails", []):
            channels.update_one(
                {"channel_id": channel_id},
                {"$push": {"emails": email}}
            )
        
    else:
        channels.insert_one({"channel_id": channel_id, "emails": [email]})
    return True

def get_channels(client,email):
    db = client["Queries"]
    channels = db["channels"]
    res = list(channels.find({"emails": email}))


    channelArray = []
    for channel in res:
        channelArray.append(channel.get("channel_id"))

    return channelArray

def get_channel(client,channel_id):
    db = client["Queries"]
    channels = db["channels"]
    res = channels.find_one({"channel_id": channel_id})
    return res