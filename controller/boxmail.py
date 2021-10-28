import json
import os, sys, datetime
from base64 import urlsafe_b64decode, urlsafe_b64encode

from six import print_
from logic import Constants
# utility functions
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

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

def search_messages(service, info_system, argv, command):
    infos = {
        "q":"",
        "maxResults": 100,
        "lbs":[],
        "includeSpamTrash":False
    }
    if(len(argv) > 0):
        list_options = ["-mr","-q","-lbs","-inc"]
        options = []
        args = []
        add_option = True
        for ar in argv:
            if(add_option):
                if(ar in list_options):
                    options.append(ar)
                    if(ar == "-inc"):
                        add_option = True
                    else:
                        add_option = False
                else:
                    printCommandInvalid(command)
                    return
            else:
                args.append(ar)
                add_option = True

        for ops in options:
            if(ops == "-mr"):
                if(len(args) == 0):
                    printCommandInvalid(command)
                    return
                value = args[0]
                args = args[1:]
                if value.isnumeric():
                    value = int(value)
                    if(value > 500 or value < 1):
                        printCommandInvalid(command)
                        return
                    else:
                        infos["maxResults"] = value
                else:
                    printCommandInvalid(command)
                    return
            elif(ops == "-q"):
                if(len(args) == 0):
                    printCommandInvalid(command)
                    return
                value = args[0]
                args = args[1:]
                infos["q"] = value
            elif(ops == "-lbs"):
                if(len(args) == 0):
                    printCommandInvalid(command)
                    return
                value = args[0]
                args = args[1:]
                infos["lbs"] = value.split(",")
            elif(ops == "-inc"):
                infos["includeSpamTrash"] = True
    print(infos)
    result = service.users().messages().list(userId='me',\
        q=infos["q"], maxResults= infos["maxResults"], labelIds=infos["lbs"], includeSpamTrash= infos["includeSpamTrash"] \
            ).execute()
            
    messages = []
    print(f'{addsuffixforfull("ID",20)}    {addsuffixforfull("ThreadId",20)}    {addsuffixforfull("LabelIds", 50)}    {addsuffixforfull("HistoryId", 15)}    {addsuffixforfull("InternalDate",20)}    {addsuffixforfull("Size",10)}    Subject')
    if 'messages' in result:
        messages = result['messages']
        for message in messages:
            printBasicInfoMessage(service, message)
    while 'nextPageToken' in result:
        print("Do you want to get next page? [Y/N]")
        inp = input()
        while(inp != "y" and inp != "Y" and inp != "n" and inp != "N"):
            print("Please input [Y/N]!")
            inp = input()
        if(inp == "y" or inp == "Y"):
            page_token = result['nextPageToken']
            result = service.users().messages().list(userId='me',\
                q=infos["q"], maxResults= infos["maxResults"], labelIds=infos["lbs"], includeSpamTrash= infos["includeSpamTrash"] \
                    , pageToken=page_token).execute()
            messages = result['messages']
            for message in messages:
                printBasicInfoMessage(service, message)
        else:
            break

def parse_parts(service, parts, folder_name, message):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()
                    print(text)
            elif mimeType == "text/html":
                # if the email part is an HTML content
                # save the HTML file and optionally open it in the browser
                if not filename:
                    filename = "index.html"
                filepath = os.path.join(folder_name, filename)
                print("Saving HTML to", filepath)
                with open(filepath, "wb") as f:
                    f.write(urlsafe_b64decode(data))
            else:
                # attachment other than a plain text or HTML
                for part_header in part_headers:
                    part_header_name = part_header.get("name")
                    part_header_value = part_header.get("value")
                    if part_header_name == "Content-Disposition":
                        if "attachment" in part_header_value:
                            # we get the attachment ID 
                            # and make another request to get the attachment itself
                            print("Saving the file:", filename, "size:", get_size_format(file_size))
                            attachment_id = body.get("attachmentId")
                            attachment = service.users().messages() \
                                        .attachments().get(id=attachment_id, userId='me', messageId=message['id']).execute()
                            data = attachment.get("data")
                            filepath = os.path.join(folder_name, filename)
                            if data:
                                with open(filepath, "wb") as f:
                                    f.write(urlsafe_b64decode(data))

def read_message(service, info_system, argv, command):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    id_mess = ""
    if(len(argv) == 1):
        id_mess = argv[0]
    else:
        printCommandInvalid(command)
        return
    message = service.users().messages().get(userId='me', id=id_mess, format='full').execute()
    idMessage = message["id"]
    threadIdMes = message["threadId"]
    labelIds = message["labelIds"]
    lbs = labelIds[0]
    for i in range(1, len(labelIds), 1):
        lbs += ", "+labelIds[i]
    internalDate = datetime.datetime.fromtimestamp(int(message["internalDate"])/ 1000).strftime("%d/%m/%Y, %H:%M:%S")
    size = get_size_format(message["sizeEstimate"])
    payload = message["payload"]
    headers = payload.get("headers")
    parts = payload.get("parts")
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
    folder_name = idMessage+"_"+subject
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    parse_parts(service, parts, folder_name, message)
    print("="*50)

def get_info_for_search_message_marking(service, info_system, argv, event):
    infos = {
        "q":"",
        "maxResults": 100,
        "lbs":[],
        "includeSpamTrash":False
    }
    if(len(argv) > 0):
        list_options = ["-q","-lbs"]
        options = []
        args = []
        add_option = True
        for ar in argv:
            if(add_option):
                if(ar in list_options):
                    options.append(ar)
                    add_option = False
                else:
                    printCommandInvalid(event)
                    return None, None, None
            else:
                args.append(ar)
                add_option = True

        for ops in options:
            if(ops == "-q"):
                if(len(args) == 0):
                    printCommandInvalid(event)
                    return
                value = args[0]
                args = args[1:]
                infos["q"] = value
            elif(ops == "-lbs"):
                if(len(args) == 0):
                    printCommandInvalid(event)
                    return
                value = args[0]
                args = args[1:]
                infos["lbs"] = value.split(",")
    print(infos)
    return service, None, infos

def mark_as_read(service, info_system, argv, command):
    service, data, infos = get_info_for_search_message_marking(service, info_system, argv,command)
    if(infos == None): return
    messages_to_mark = []
    result = service.users().messages().list(userId = "me", q=infos["q"], labelIds=infos["lbs"]).execute()
    if "messages" in result:
        messages_to_mark.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',\
            q=infos["q"], labelIds=infos["lbs"] \
                , pageToken=page_token).execute()
        if "messages" in result:
            messages_to_mark.extend(result["messages"])
    data =  service.users().messages().batchModify(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_mark ],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()
    print(json.dumps(data))

def mark_as_read_byid(service, info_system, argv, command):
    if(len(argv) != 1):
        printCommandInvalid(command)
        return
    id_mess = argv[0]
    return service.users().messages().batchModify(
      userId='me',
      body={
          'ids': [id_mess],
          'removeLabelIds': ['UNREAD']
      }
    ).execute()

def mark_as_unread(service, info_system, argv, command):
    service, data, infos = get_info_for_search_message_marking(service, info_system, argv,command)
    if(infos == None): return
    messages_to_mark = []
    result = service.users().messages().list(userId = "me", q=infos["q"], labelIds=infos["lbs"]).execute()
    if "messages" in result:
        messages_to_mark.extend(result["messages"])
    while "nextPageToken" in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',\
            q=infos["q"], labelIds=infos["lbs"] \
                , pageToken=page_token).execute()
        if "messages" in result:
            messages_to_mark.extend(result["messages"])
    # add the label UNREAD to each of the search results
    data =  service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [ msg['id'] for msg in messages_to_mark ],
            'addLabelIds': ['UNREAD']
        }
    ).execute()
    print(json.dumps(data))

def mark_as_unread_byid(service, info_system, argv, command):
    if(len(argv) != 1):
        printCommandInvalid(command)
        return
    id_mess = argv[0]
    # add the label UNREAD to each of the search results
    return service.users().messages().batchModify(
        userId='me',
        body={
            'ids': [id_mess],
            'addLabelIds': ['UNREAD']
        }
    ).execute()

def delete_messages(service, info_system, argv, command):
    if(len(argv) != 1):
        printCommandInvalid(command)
        return
    ids = argv[0].split(",")
    if(len(ids) == 0):
        printCommandInvalid(command)
        return
    if(len(ids) == 1):
        id = ids[0]
        data = service.users().messages().delete(userId="me", id= id).execute()
        print(data)
    else:
        id_batch = []
        for id in ids:
            if(len(id) > 0):
                id_batch.append(id)
        if(len(id_batch) == 0):
            printCommandInvalid(command)
            return
        data = service.users().messages().batchDelete(
            userId="me",
            body={
                "ids": id_batch
            }
        ).execute()
        print(data)

def trash(service, info_system, argv, command):
    if(len(argv) != 1):
        printCommandInvalid(command)
        return
    id = argv[0]
    data = service.users().messages().trash(userId="me", id = id).execute()
    print(data)

def untrash(service, info_system, argv, command):
    if(len(argv) != 1):
        printCommandInvalid(command)
        return
    id = argv[0]
    data = service.users().messages().untrash(userId="me", id = id).execute()
    print(data)

def emptytrash(service, info_system, argv, command):
    if(len(argv) > 0):
        printCommandInvalid(command)
        return
    print("Are you sure with this command? Your mail in trash wild be deleted permanently!")
    print("Please comfirm [Y/N]")
    confirm = input()
    if(confirm == "y" or confirm=="Y"):
        pass
    else:
        return
    threads = []
    result = service.users().threads().list(
        userId = "me",
        q = "in:trash",
    ).execute()
    if "threads" in result:
        threads.extend(result["threads"])
    while "nextPageToken" in result:
        page_token = result["nextPageToken"]
        result = service.users().threads().list(
            userId = "me",
            q="in:trash",
            pageToken = page_token
        ).execute()
        if "threads" in result:
            threads.extend(result["threads"])
    idThreads = []
    for thread in threads:
        print("Delete permanently {} ...".format(thread["id"]))
        service.users().threads().delete(userId="me", id=thread["id"]).execute()

def addLabels(service, info_system, argv, command):
    if(len(argv) == 2):
        ids = argv[0].split(",")
        labels = argv[1].split(",")
        data = service.users().messages().batchModify(
            userId = "me",
            body={
                "ids": ids,
                "addLabelIds": labels
            }
        ).execute()
        print(data)
    else:
        printCommandInvalid(command)

def removeLabels(service, info_system, argv, command):
    if(len(argv) == 2):
        ids = argv[0].split(",")
        labels = argv[1].split(",")
        data = service.users().messages().batchModify(
            userId = "me",
            body={
                "ids": ids,
                "removeLabelIds": labels
            }
        ).execute()
        print(data)
    else:
        printCommandInvalid(command)

def printBasicInfoMessage(service, message):
    message = service.users().messages().get(userId='me', id=message["id"], format='full').execute()
    messId = message["id"]
    threadId = message["threadId"]
    lbs = message["labelIds"]
    s = lbs[0]
    for i in range(1, len(lbs), 1):
        s += ", "+lbs[i]
    snippet = message["snippet"]
    historyId = message["historyId"]
    internalDate = datetime.datetime.fromtimestamp(int(message["internalDate"])/1000).strftime("%d/%m/%Y, %H:%M:%S")
    sizeEstimate = get_size_format(int(message["sizeEstimate"]))
    payload = message['payload']
    headers = payload.get("headers")
    subj = ""
    for header in headers:
        name = header.get("name")
        value = header.get("value")
        if(name.lower() == "subject"):
            subj = value
    print(f"{addsuffixforfull(messId,20)}    {addsuffixforfull(threadId,20)}    {addsuffixforfull(s,50)}    {addsuffixforfull(historyId,15)}    {addsuffixforfull(''+internalDate,20)}    {addsuffixforfull(sizeEstimate,10)}    {subj}")

def addsuffixforfull(mess, size):
    while(len(mess) < size):
        mess += " "
    return mess

def printCommandInvalid(command):
    print(f"Syntax command '{command}' invalid! Please view")
    print(Constants.MESSAGE_SEPARATOR)
    print(Constants.MESSAGE_SYNTAX)