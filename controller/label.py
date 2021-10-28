import json
import os, sys, datetime
from base64 import urlsafe_b64decode, urlsafe_b64encode
from typing import Tuple
from logic import Constants


def get_instance_label(argv, command, label):
    id = ""
    if(command != "createlabel"):
        if(len(argv) == 0):
            printCommandInvalid(command)
            return None
        id = argv[0]
        argv = argv[1:]
    if(len(argv) == 0):
        print("Not found info label to execute")
        return None
    list_value_lv = ["labelShow", "labelShowIfUnread", "labelHide", "empty"]
    list_value_mv = ["show", "hide", "empty"]
    list_ops = ["-n", "-lv", "-mv", "-bg", "-tc"]
    options = []
    args = []
    add_option = True
    for ar in argv:
        if(add_option):
            if(ar in list_ops):
                options.append(ar)
                add_option = False
            else:
                printCommandInvalid(command)
                return None
        else:
            args.append(ar)
            add_option = True
    for op in options:
        if(op == "-n"):
            if(len(args)==0):
                printCommandInvalid(command)
                return None
            label["name"] = args[0].upper()
            args = args[1:]
        elif(op == "-lv"):
            if(len(args) == 0):
                printCommandInvalid(command)
                return None
            if(args[0] in list_value_lv):
                if(args[0] == "empty"):
                    if("labelListVisibility" in label):
                        label.pop("labelListVisibility")
                else:
                    label["labelListVisibility"] = args[0]
                args=args[1:]
            else:
                printCommandInvalid(command)
                return None
        elif(op == "-mv"):
            if(len(args) == 0):
                printCommandInvalid(command)
                return None
            if(args[0] in list_value_mv):
                if(args[0] == "empty"):
                    if("messageListVisibility" in label):
                        label.pop("messageListVisibility")
                else:
                    label["messageListVisibility"] = args[0]
                args=args[1:]
            else:
                printCommandInvalid(command)
                return None
        elif(op == "-bg"):
            if(len(args) == 0):
                printCommandInvalid(command)
                return None
            if "color" not in label:
                label["color"] = {}
            label["color"]["backgroundColor"] = args[0]
            args = args[1:]
        elif(op == "-tc"):
            if(len(args) == 0):
                printCommandInvalid(command)
                return None
            if "color" not in label:
                label["color"] = {}
            label["color"]["textColor"] = args[0]
            args = args[1:]

    if(label["name"] == ""):
        print("name label not found!")
        return None

    return label

def create(service, info_system, argv, command):
    label = {
        "name": "",
        "color":{
            "textColor": "",
            "backgroundColor": ""
        }
    }
    label = get_instance_label(argv, command, label)
    if(label == None):
        return
    print(label)
    label = service.users().labels().create(
        userId="me",
        body=label
    ).execute()
    printInfoLabel(service,label)

def delete(service, info_system, argv, command):
    if(len(argv) != 1):
        printCommandInvalid(command)
        return
    data = service.users().labels().delete(
        userId="me",
        id=argv[0]
    ).execute()
    print(data)

def get(service, info_system, argv, command):
    if(len(argv) != 1):
        printCommandInvalid(command)
        return
    label = service.users().labels().get(
        userId="me",
        id=argv[0]
    ).execute()
    printInfoLabel(service,label)

def search(service, info_system, argv, command):
    result = service.users().labels().list(
        userId = "me"
    ).execute()
    labels = []
    if("labels" in result):
        labels.extend(result["labels"])
    for label in labels:
        printInfoLabel(service,label)

def patch(service, info_system, argv, command):
    if(len(argv) == 0):
        printCommandInvalid(command)
        return
    label = service.users().labels().get(
        userId="me",
        id=argv[0]
    ).execute()
    label = get_instance_label(argv, command, label)
    if(label == None):
        return
    label = service.users().labels().patch(
        userId="me",
        id=argv[0],
        body=label
    ).execute()
    printInfoLabel(service,label)

def update(service, info_system, argv, command):
    if(len(argv) == 0):
        printCommandInvalid(command)
        return
    label = service.users().labels().get(
        userId="me",
        id=argv[0]
    ).execute()
    label = get_instance_label(argv, command, label)
    if(label == None):
        return
    label = service.users().labels().update(
        userId="me",
        id=argv[0],
        body=label
    ).execute()
    printInfoLabel(service,label)

def printInfoLabel(service,label):
    id = label["id"]
    label = service.users().labels().get(
        userId = "me",
        id=id
    ).execute()
    name = label["name"]
    labelListVisibility = ""
    if("labelListVisibility" in label):
        labelListVisibility = label["labelListVisibility"]

    messageListVisibility = ""
    if("messageListVisibility" in label):
        messageListVisibility = label["messageListVisibility"]

    backgroundColor=""
    textColor=""
    if("color" in label):
        color = label["color"]
        if("backgroundColor" in color):
            backgroundColor = color["backgroundColor"]
        if("textColor" in color):
            textColor = color["textColor"]

    messagesTotal=""
    if("messagesTotal" in label):
        messagesTotal = label["messagesTotal"]

    messagesUnread=""
    if("messagesUnread" in label):
        messagesUnread = label["messagesUnread"]
    
    threadsTotal=""
    if("threadsTotal" in label):
        threadsTotal = label["threadsTotal"]
    
    threadsUnread=""
    if("threadsUnread" in label):
        threadsUnread = label["threadsUnread"]

    typel=""
    if("type" in label):
        typel = label["type"]

    print(f"ID:                     {id}")
    print(f"Name:                   {name}")
    print(f"LabelListVisibility:    {labelListVisibility}")
    print(f"MessageListVisibility:  {messageListVisibility}")
    print(f"BackgroundColor:        {backgroundColor}")
    print(f"TextColor:              {textColor}")
    print(f"MessagesTotal:          {messagesTotal}")
    print(f"MessagesUnread:         {messagesUnread}")
    print(f"ThreadsTotal:           {threadsTotal}")
    print(f"ThreadsUnread:          {threadsUnread}")
    print(f"Type:                   {typel}")
    print(Constants.MESSAGE_SEPARATOR)

def printCommandInvalid(command):
    print(f"Syntax command '{command}' invalid! Please view")
    print(Constants.MESSAGE_SEPARATOR)
    print(Constants.MESSAGE_SYNTAX)