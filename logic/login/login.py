from logging import info
import os
import pickle
#import gmail api
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encode and decode message with base64

import logic.Constants as cons


def load_infosystem():
    info_system = {}
    with open("datalog/infosystem.txt","r") as file:
        strfile = file.readline()
        while(strfile != ""):
            strarray = strfile.split("=")
            info_system[strarray[0].strip()] = strarray[1].strip()
            strfile = file.readline()
        file.close()
    return info_system

def save_infosystem(info_system):
    with open("datalog/infosystem.txt", "w") as file:
        for key in info_system.keys():
            strfile = f"{key}={info_system[key]}\n"
            file.write(strfile)
            file.flush()
        file.close()

def gmail_authenticate(email=""):
    creds = None
    check = False
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(f"datalog/{email}_token.pickle"):
        with open(f"datalog/{email}_token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', cons.SCOPES)
            creds = flow.run_local_server(port=0)
            check = True
    service =  build('gmail', 'v1', credentials=creds)
    data = service.users().getProfile(userId="me").execute()
    email = data["emailAddress"]
    if(check):
        # save the credentials for the next run
        with open(f"datalog/{email}_token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return service, data


def login(email=None, info_system=None):
    if(info_system == None):
        raise ValueError("Info System is not None")
    if(email == None):
        service, data = gmail_authenticate()
        if(info_system["history_email"].find(data["emailAddress"]) < 0):
            if(info_system["history_email"] == ""):
                info_system["history_email"] = data["emailAddress"]
            else:
                info_system["history_email"] += "," + data["emailAddress"]
        info_system["last_login"] = data["emailAddress"]
        info_system["current_login"] = data["emailAddress"]
        save_infosystem(info_system)
        return service, data, info_system
    else:
        service, data = gmail_authenticate(email)
        info_system["last_login"] = data["emailAddress"]
        info_system["current_login"] = data["emailAddress"]
        save_infosystem(info_system)
        return service, data, info_system


def removeAllCache(info_system=None):
    if(info_system == None):
        raise ValueError("Info System is not null")
    for email in info_system["history_email"].split(","):
        if(os.path.exists(f"datalog/{email}_token.pickle")):
            os.remove(f"datalog/{email}_token.pickle")
    info_system["last_login"] = ''
    info_system["history_email"] = ''
    info_system["current_login"] = ''
    save_infosystem(info_system)
    return info_system
