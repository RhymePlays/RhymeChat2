var Elements = {
    "allChatRooms": document.getElementById("allChatRooms"),
    "allTextItems": document.getElementById("allTextItems"),
    "chatRoomAdmins": document.getElementById("rightPanelAdmins"),
    "chatRoomMembers": document.getElementById("rightPanelMembers"),
}

function populateChatRoomItems(roomIDs){
    Elements.allChatRooms.innerHTML = "";
    for (idIndex in roomIDs){
        let chatRoomItem = document.createElement("div");
        chatRoomItem.className = "chatRoomItem";
        chatRoomItem.innerText = roomIDs[idIndex];
        chatRoomItem.onclick = "";
        Elements.allChatRooms.append(chatRoomItem);
    }
}

function populateChatRoomAdmins(admins){
    Elements.chatRoomAdmins.innerHTML = "";
    for (adminIndex in admins){
        let adminItem = document.createElement("div");
        adminItem.className = "rightPanelUserItem";
        
        let adminItemName = document.createElement("div");
        adminItemName.className = "rightPanelUserItemName";
        adminItemName.innerText = admins[adminIndex];
        
        let adminItemAction = document.createElement("div");
        adminItemAction.className = "removeAdminButton";
        adminItemAction.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M11 5v11.17l-4.88-4.88c-.39-.39-1.03-.39-1.42 0-.39.39-.39 1.02 0 1.41l6.59 6.59c.39.39 1.02.39 1.41 0l6.59-6.59c.39-.39.39-1.02 0-1.41-.39-.39-1.02-.39-1.41 0L13 16.17V5c0-.55-.45-1-1-1s-1 .45-1 1z"/></svg>';
        adminItemAction.onclick = "";
        
        adminItem.append(adminItemName, adminItemAction);

        Elements.chatRoomAdmins.append(adminItem);
    }
}

function populateChatRoomMembers(memebers){
    Elements.chatRoomMembers.innerHTML = "";
    for (memeberIndex in memebers){
        let memberItem = document.createElement("div");
        memberItem.className = "rightPanelUserItem";
        
        let memberItemName = document.createElement("div");
        memberItemName.className = "rightPanelUserItemName";
        memberItemName.innerText = memebers[memeberIndex];
        
        let memberItemAction = document.createElement("div");
        memberItemAction.className = "makeAdminButton";
        memberItemAction.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M13 19V7.83l4.88 4.88c.39.39 1.03.39 1.42 0 .39-.39.39-1.02 0-1.41l-6.59-6.59c-.39-.39-1.02-.39-1.41 0l-6.6 6.58c-.39.39-.39 1.02 0 1.41.39.39 1.02.39 1.41 0L11 7.83V19c0 .55.45 1 1 1s1-.45 1-1z"/></svg>';
        memberItemAction.onclick = "";
        
        memberItem.append(memberItemName, memberItemAction);

        Elements.chatRoomMembers.append(memberItem);
    }
}

function populateChat(texts){
    Elements.allTextItems.innerHTML = "";
    for (text in texts){
        let textItem = document.createElement("div");
        textItem.className = "textItem";
        
        let textItemNameNDate = document.createElement("div");
        textItemNameNDate.className = "textItemNameNDate";
        let textItemUsername = document.createElement("div");
        textItemUsername.className = "textItemUsername";
        textItemUsername.innerText = texts[text][0];
        let textItemTime = document.createElement("div");
        textItemTime.className = "textItemTime";
        textItemTime.innerText = texts[text][2];
        textItemNameNDate.append(textItemUsername, textItemTime)
    
        let textItemBody = document.createElement("div");
        textItemBody.className = "textItemBody";
        textItemBody.innerText = texts[text][1];
    
        textItem.append(document.createElement("hr"), textItemNameNDate, textItemBody)
    
        Elements.allTextItems.append(textItem)
    }
}