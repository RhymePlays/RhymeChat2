from flask import Flask
import os, time, json, hashlib, threading

# Initing Flask
app = Flask(__name__)

# Variables
hashSalt = "LongLiveMyAnimeWaifus"

allowedUsernameChars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "_", "."]

autoSave = True

accounts = {
    # "username": {
    #     "index": 0,
    #     "password": "pass1234",
    #     "joined": 0.0,
    #     "chats": []
    # },
    # "rhyme": {
    #     "index": 1,
    #     "password": "pass1234",
    #     "joined": 0.0,
    #     "chats": ["0"]
    # },
    # "ryan": {
    #     "index": 2,
    #     "password": "pass1234",
    #     "joined": 0.0,
    #     "chats": ["0"]
    # }
}

chats = {
    # "0": {
    #     "users": ["rhyme", "ryan"],
    #     "admins": ["rhyme"],
    #     "settings": {},
    #     "texts": [("hellow", "body"), ("username", "body")]
    # }
}

webUI = ""

# Functions
def usernameCharCheck(username):
    username=username.lower()
    for char in username:
        if char not in allowedUsernameChars:
            return False
    return True

def authCheck(username, password):
    if username in accounts:
        if accounts[username]["password"] == hashlib.sha256((password+hashSalt).encode("ascii")).hexdigest():
            return True
        else:
            return False
    else:
        return False

def loadDatabase():
    global accounts, chats
    try:
        with open("data.json", "r") as f:
            data = json.loads(f.read())
            accounts = data["accounts"]
            chats = data["chats"]
    except:
        print("Failed to load database")

def autoSaveDatabase():
    while autoSave:
        time.sleep(300)
        try:
            with open("data.json", "w") as f:
                f.write(json.dumps({"accounts": accounts,"chats": chats}))
            print("Auto-saved database "+str(time.time()))
        except:
            print("Failed to auto-save database "+str(time.time()))

def loadWebUI():
    global webUI
    try:
        with open("index.html", "r") as f:
            webUI = f.read()
    except:
        print("Failed to load webUI")

# Routes
@app.route("/")
def root():
    return webUI

@app.route("/api")
def api():
    return """
    Konnichiwa Sekai</br>
    Welcome to RhymeChat2 API. This server operates in a REST fashion.</br>
    </br>
    Available command:</br>
    1) Signing up -> "/signup/username/password/email"</br>
    2) Creating Chat Room -> "/createChatRoom/username/password"</br>
    3) Getting Chat Rooms -> "/getChatRooms/username/password"</br>
    4) Add someone to Chat Room -> "/addToChatRoom/username/password/chatId/personToAdd"</br>
    5) Making someone Admin -> "/makeAdmin/username/password/chatId/personToMakeAdmin"</br>
    6) Removong someone from Admin -> "/removeAdmin/username/password/chatId/personToRemoveFromAdmin"</br>
    7) Get Chat Room data -> "/getChatRoomData/username/password/chatId"</br>
    8) Send text to Chat Room -> "/send/username/password/chatId/body"</br>
    9) Recive texts from a Chat Room -> "/recv/username/password/chatId/fromIndex/toIndex"</br>
    10) Save to DB -> "/saveData/code"
    """

@app.route("/saveData/<code>")
def saveDatabase(code):
    if code == "LongLiveMyAnimeWaifus":
        try:
            with open("data.json", "w") as f:
                f.write(json.dumps({"accounts": accounts,"chats": chats}))
            return "Successfully saved"
        except:
            return "Failed to save"
    else:
        return "Failed to save"

@app.route("/signup/<username>/<password>/<email>")
def signup(username, password, email):
    if usernameCharCheck(username) and (username not in accounts) and (len(username) >= 4) and (len(username) <= 18) and (len(email) > 1) and (len(email) <= 320):
        if len(password) >= 8 and len(password) <= 64:
            accounts[username] = {"password": hashlib.sha256((password+hashSalt).encode("ascii")).hexdigest(), "email": email, "joined": time.time(), "chats": []}
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
        return "error"

@app.route("/createChatRoom/<username>/<password>")
def createChatRoom(username, password):
    if authCheck(username, password):
        chatId=str(len(chats))
        chats[chatId]={"users": [username], "admins":[username], "settings": {}, "texts": []}
        accounts[username]["chats"].append(chatId)
        return chatId
    else:
        return "error"

@app.route("/addToChatRoom/<username>/<password>/<chatId>/<personToAdd>")
def addToChatRoom(chatId, username, password, personToAdd):
    if authCheck(username, password) and (personToAdd in accounts) and (chatId in chats):
        if username in chats[chatId]["admins"]:
            chats[chatId]["users"].append(personToAdd)
            accounts[personToAdd]["chats"].append(chatId)
            return "success"
        else:
            return "error"
    else:
        return "error"

@app.route("/makeAdmin/<username>/<password>/<chatId>/<personToMakeAdmin>")
def makeAdmin(chatId, username, password, personToMakeAdmin):
    if authCheck(username, password) and (personToMakeAdmin in accounts) and (chatId in chats):
        if (username in chats[chatId]["admins"]) and (personToMakeAdmin not in chats[chatId]["admins"]) and (personToMakeAdmin in chats[chatId]["users"]):
            chats[chatId]["admins"].append(personToMakeAdmin)
            return "success"
        else:
            return "error"
    else:
        return "error"

@app.route("/removeAdmin/<username>/<password>/<chatId>/<personToRemoveFromAdmin>")
def removeAdmin(chatId, username, password, personToRemoveFromAdmin):
    if authCheck(username, password) and (personToRemoveFromAdmin in accounts) and (chatId in chats):
        if (username in chats[chatId]["admins"]) and (personToRemoveFromAdmin in chats[chatId]["admins"]) and (personToRemoveFromAdmin in chats[chatId]["users"]):
            if len(chats[chatId]["admins"])>1:
                chats[chatId]["admins"].remove(personToRemoveFromAdmin)
                return "success"
            else:
                return "error"
        else:
            return "error"
    else:
        return "error"

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
            return "error"
    else:
        return "error"

@app.route("/send/<username>/<password>/<chatId>/<body>")
def send(chatId, username, password, body):
    if authCheck(username, password) and (chatId in chats) and (len(body)>=1) and (len(body)<=256):
        if username in chats[chatId]["users"]:
            chats[chatId]["texts"].insert(0, (username, body, time.time()))
            return "success"
        else:
            return "error"
    else:
        return "error"

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
                return "error"
        else:
            return "error"
    else:
        return "error"

# Starting point of the app
if __name__ == "__main__":
    loadDatabase();loadWebUI()
    savingThread = threading.Thread(target=autoSaveDatabase);savingThread.start()
    app.run(port=80, debug=True)