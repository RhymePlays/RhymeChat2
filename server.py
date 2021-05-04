from flask import Flask
import os, time, json

# Initing Flask
app = Flask(__name__)

# Variables
accounts = {
    "username": {
        "index": 0,
        "password": "pass1234",
        "joined": 0.0,
        "chats": []
    },
    "rhyme": {
        "index": 1,
        "password": "pass1234",
        "joined": 0.0,
        "chats": ["0"]
    },
    "ryan": {
        "index": 2,
        "password": "pass1234",
        "joined": 0.0,
        "chats": ["0"]
    }
}

chats = {
    "0": {
        "users": ["rhyme", "ryan"],
        "admins": ["rhyme"],
        "settings": {},
        "texts": [("hellow", "body"), ("username", "body")]
    }
}

# Functions
def authCheck(username, password):
    if username in accounts:
        if accounts[username]["password"] == password:
            return True
        else:
            return False
    else:
        return False

# Routes
@app.route("/")
def root():
    return "Konnichiwa Sekai"

@app.route("/signup/<username>/<password>")
def signup(username, password):
    if username not in accounts and len(username) >= 4:
        if len(password) >= 8: 
            accounts[username] = {"index": len(accounts), "password": password, "joined": time.time(), chats: []}
            return "Account successfully created"
        else:
            return "Password too short"
    else:
        return "Username already exists or username too short"

@app.route("/getChatRooms/<username>/<password>")
def getChatRooms(username, password):
    if authCheck(username, password):
        return json.dumps(accounts[username]["chats"])
    else:
        return "Error getting chats"

@app.route("/createChatRoom/<username>/<password>")
def createChatRoom(username, password):
    if authCheck(username, password):
        chatId=str(len(chats))
        chats[chatId]={"users": [username], "admins":[username], "settings": {}, "texts": []}
        accounts[username]["chats"].append(chatId)
        return chatId
    else:
        return "Error creating chat"

@app.route("/addToChatRoom/<username>/<password>/<chatId>/<personToAdd>")
def addToChatRoom(chatId, username, password, personToAdd):
    if authCheck(username, password) and (personToAdd in accounts) and (chatId in chats):
        if username in chats[chatId]["admins"]:
            chats[chatId]["users"].append(personToAdd)
            accounts[personToAdd]["chats"].append(chatId)
            return "User successfully added"
        else:
            return "Admin role needed"
    else:
        return "Error adding to chat"

@app.route("/makeAdmin/<username>/<password>/<chatId>/<personToMakeAdmin>")
def makeAdmin(chatId, username, password, personToMakeAdmin):
    if authCheck(username, password) and (personToMakeAdmin in accounts) and (chatId in chats):
        if (username in chats[chatId]["admins"]) and (personToMakeAdmin not in chats[chatId]["admins"]) and (personToMakeAdmin in chats[chatId]["users"]):
            chats[chatId]["admins"].append(personToMakeAdmin)
            return "User successfully made admin"
        else:
            return "Admin role needed or user already admin"
    else:
        return "Error making admin"

@app.route("/removeAdmin/<username>/<password>/<chatId>/<personToRemoveFromAdmin>")
def removeAdmin(chatId, username, password, personToRemoveFromAdmin):
    if authCheck(username, password) and (personToRemoveFromAdmin in accounts) and (chatId in chats):
        if (username in chats[chatId]["admins"]) and (personToRemoveFromAdmin in chats[chatId]["admins"]) and (personToRemoveFromAdmin in chats[chatId]["users"]):
            if len(chats[chatId]["admins"])>1:
                chats[chatId]["admins"].remove(personToRemoveFromAdmin)
                return "Successfully removed user from admin"
            else:
                return "Cannot remove the only admin"
        else:
            return "Admin role needed or user not admin"
    else:
        return "Error removing admin"

@app.route("/getChatRoomData/<username>/<password>/<chatId>")
def getChatRoomData(username, password, chatId):
    if authCheck(username, password) and (chatId in chats):
        if username in chats[chatId]["users"]:
            return json.dumps({
                "users": chats[chatId]["users"],
                "admins": chats[chatId]["admins"],
                "settings": chats[chatId]["settings"]
            })
        else:
            return "Error getting data"
    else:
        return "Error getting data"

@app.route("/send/<username>/<password>/<chatId>/<body>")
def send(chatId, username, password, body):
    if authCheck(username, password) and chatId in chats:
        if username in chats[chatId]["users"]:
            chats[chatId]["texts"].insert(0, (username, body))
            return "Message successfully sent"
        else:
            return "Error sending message"
    else:
        return "Error sending message"

@app.route("/recv/<username>/<password>/<chatId>/<fromIndex>/<toIndex>")
def recieve(chatId, username, password, fromIndex, toIndex):
    if authCheck(username, password) and chatId in chats:
        if username in chats[chatId]["users"]:
            try:
                fromIndex=int(fromIndex);toIndex=int(toIndex)
                returnValue=[]
                for index in range(fromIndex, toIndex):
                    try:
                        returnValue.append(chats[chatId]["texts"][index])
                    except:
                        return json.dumps(returnValue)
                return json.dumps(returnValue)
            except:
                return "Error getting chat"
        else:
            return "Error getting chat"
    else:
        return "Error getting chat"

# Starting point of the app
if __name__ == "__main__":
    app.run(port=5050, debug=True)