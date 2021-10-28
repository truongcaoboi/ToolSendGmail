import json
from logging import info
import os, sys, datetime
from base64 import urlsafe_b64decode, urlsafe_b64encode
from logic import Constants
from controller import sendmail, boxmail
from logic.sendmail.SendMail import SendMail

def create(service, info_system, argv, command):
    factory_send = SendMail(service)
    link_defaul = "content_send_mail.json"
    if(len(argv)>0):
        if(len(argv) == 2):
            if(argv[0] == "-f"):
                if(os.path.exists(argv[1])):
                    link_defaul = argv[1]
                else:
                    print("Not found file {}!".format(argv[1]))
                    return
            else:
                printCommandInvalid(command)
                return
        else:
            printCommandInvalid(command)
            return
    userId, destination, email_send, cc, bcc, subject, body, attachments, sub_type = sendmail.read_file_config_mail(link_defaul,info_system)
    body_mess = factory_send.build_message(destination,email_send, cc, bcc, subject, body, attachments, sub_type)
    draft = {
        "message": body_mess
    }
    data = service.users().drafts().create(
        userId = userId,
        body=draft
    ).execute()
    print(json.dumps(data))

def delete(service, info_system, argv, command):
    if(len(argv) == 1):
        id = argv[0]
        data = service.users().drafts().delete(
            userId = "me",
            id= id
        ).execute()
        print(data)
    else:
        printCommandInvalid(command)

def deleteAll(service, info_system, argv, command):
    if(len(argv) == 0):
        drafts = []
        result = service.users().drafts().list(
            userId = "me"
        ).execute()
        if "drafts" in result:
            drafts.extend(result["drafts"])
        while "nextPageToken" in result:
            page_token = result["nextPageToken"]
            result = service.users().drafts().list(
                userId = "me",
                pageToken=page_token
            ).execute()
            if "drafts" in result:
                drafts.extend(result["drafts"])
        for draft in drafts:
            print("Delete draft {}".format(draft["id"]))
            service.users().drafts().delete(
                userId = "me",
                id= draft["id"]
            ).execute()
    else:
        printCommandInvalid(command)

def read(service, info_system, argv, command):
    if(len(argv) == 1):
        message, subject = printInfoBaseDraft(service,argv[0], True)
        payload = message["payload"]
        folder_name = message["id"]+"_"+subject
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        parts = payload["parts"]
        boxmail.parse_parts(service, parts, folder_name, message)
        print(Constants.MESSAGE_SEPARATOR)
    else:
        printCommandInvalid(command)

def search(service, info_system, argv, command):
    infos = {
        "q":"",
        "mr": 100,
        "inc": False
    }
    if(len(argv)>0):
        list_op = ["-q", "-mr", "-inc"]
        options = []
        args = []
        add_options = True
        for arg in argv:
            if(add_options):
                if(arg in list_op):
                    options.append(arg)
                    if(arg == "-inc"):
                        add_options = True
                    else:
                        add_options = False
                else:
                    printCommandInvalid(command)
                    return
            else:
                args.append(arg)
                add_options = True
        for op in options:
            if(op == "-inc"):
                infos["inc"] = True
            elif(op == "-mr"):
                if(len(args) == 0):
                    printCommandInvalid(command)
                    return
                if(args[0].isnumeric()):
                    infos["mr"] = args[0]
                    args = args[1:]
                else:
                    printCommandInvalid(command)
                    return
            elif(op == "-q"):
                if(len(args) == 0):
                    printCommandInvalid(command)
                    return
                infos["q"] = args[0]
                args = args[1:]
        

    result = service.users().drafts().list(
        userId = "me",
        q=infos["q"],
        maxResults=infos["mr"],
        includeSpamTrash=infos["inc"]
    ).execute()

    if "drafts" in result:
        for draft in result["drafts"]:
            printInfoBaseDraft(service, draft["id"])
    while "nextPageToken" in result:
        print("Do you want to view next pages? [Y/N]")
        next = input()
        if(next == "y" or next == "Y"):
            result = service.users().drafts().list(
                userId = "me",
                q=infos["q"],
                maxResults=infos["mr"],
                includeSpamTrash=infos["inc"],
                pageToken=result["nextPageToken"]
            ).execute()
            if "drafts" in result:
                for draft in result["drafts"]:
                    printInfoBaseDraft(service, draft["id"])
        else:
            break
        

            

def send(service, info_system, argv, command):
    if(len(argv) == 1):
        id = argv[0]
        draft = service.users().drafts().get(
            userId="me",
            id=id
        ).execute()

        data = service.users().drafts().send(
            userId = "me",
            body=draft
        ).execute()
        print(json.dumps(data))
    else:
        printCommandInvalid(command)


def update(service, info_system, argv, command):
    factory_send = SendMail(service)
    link_defaul = "content_send_mail.json"
    id = ""
    if(len(argv)>0):
        if(len(argv) == 3):
            id = argv[0]
            if(argv[1] == "-f"):
                if(os.path.exists(argv[2])):
                    link_defaul = argv[2]
                else:
                    print("Not found file {}!".format(argv[1]))
                    return
            else:
                printCommandInvalid(command)
                return
        else:
            if(len(argv) == 1):
                id = argv[0]
            else:
                printCommandInvalid(command)
                return
    userId, destination, email_send, cc, bcc, subject, body, attachments, sub_type = sendmail.read_file_config_mail(link_defaul, info_system)
    body_mess = factory_send.build_message(destination,email_send, cc, bcc, subject, body, attachments, sub_type)
    draft = {
        "id":id,
        "message": body_mess
    }
    data = service.users().drafts().create(
        userId = userId,
        body=draft
    ).execute()
    print(json.dumps(data))


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def addsuffixforfull(mess, size):
    while(len(mess) < size):
        mess += " "
    return mess

def printInfoBaseDraft(service, id, hasreturn=False):
    draft = service.users().drafts().get(
        userId="me",
        id=id,
        format="full"
    ).execute()
    idDraft = draft["id"]
    message = draft["message"]
    idMessage = message["id"]
    threadIdMes = message["threadId"]
    labelIds = message["labelIds"]
    lbs = labelIds[0]
    for i in range(1, len(labelIds), 1):
        lbs += ", "+labelIds[i]
    internalDate = datetime.datetime.fromtimestamp(int(message["internalDate"])/ 1000).strftime("%d/%m/%Y, %H:%M:%S")
    size = get_size_format(message["sizeEstimate"])
    payload = message["payload"]
    headers = payload["headers"]
    email_to = ""
    email_from = ""
    subject = ""
    cc = ""
    bcc = ""
    for header in headers:
        name = header["name"]
        value = header["value"]
        if(name.lower() == "to"):
            email_to = value
        elif(name.lower() == "from"):
            email_from = value
        elif(name.lower() == "cc"):
            cc = value
        elif(name.lower() == "bcc"):
            bcc = value
        elif(name.lower() == "subject"):
            subject = value

    print(f"Draft Id:       {idDraft}")
    print(f"Message Id:     {idMessage}")
    print(f"Thread Id:      {threadIdMes}")
    print(f"LabelIds:       {lbs}")
    print(f"Internal Date:  {internalDate}")
    print(f"Size:           {size}")
    print(f"From:           {email_from}")
    print(f"To:             {email_to}")
    print(f"CC:             {cc}")
    print(f"BCC:            {bcc}")
    print(f"Subject:        {subject}")
    print(Constants.MESSAGE_SEPARATOR)
    if(hasreturn):
        return message, subject

def printCommandInvalid(command):
    print(f"Syntax command '{command}' invalid! Please view")
    print(Constants.MESSAGE_SEPARATOR)
    print(Constants.MESSAGE_SYNTAX)
