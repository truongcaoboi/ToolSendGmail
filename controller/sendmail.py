
from logic.sendmail.SendMail import SendMail
from logic.login import login
from logic import Constants
import os, json

def read_file_config_mail(link_default, info_system):
    strobj = ""
    with open(link_default, "r") as file:
        textfile = file.readline()
        while(textfile != ""):
            strobj += textfile
            textfile = file.readline()
        file.close()
    object_mess = json.loads(strobj)

    userId = "me"
    destination = ""
    for des in object_mess["to"]:
        if(len(destination) == 0):
            destination += des
        else:
            destination += ","+des
    email_send = info_system["current_login"]
    cc = ""
    for email in object_mess["cc"]:
        if(len(cc) == 0):
            cc += email
        else:
            cc += ","+email
    bcc = ""
    for email in object_mess["bcc"]:
        if(len(bcc) == 0):
            bcc += email
        else:
            bcc += ","+email
    subject = object_mess["subject"]
    body = ""
    sub_type = object_mess["type"]
    if(sub_type == "plain"):
        body = object_mess["content"]
    elif(sub_type == "html"):
        with open(object_mess["content"], "r") as file:
            textfile = file.readline()
            while(textfile != ""):
                body += textfile
                textfile = file.readline()
    attachments = object_mess["attach"]
    return userId, destination, email_send, cc, bcc, subject, body, attachments, sub_type

def sendMail(service, info_system, argv, command):
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
    userId, destination, email_send, cc, bcc, subject, body, attachments, sub_type = read_file_config_mail(link_defaul, info_system)
    data = factory_send.send_message(userId,destination,email_send,cc, bcc,subject,body,attachments, sub_type)
    print(json.dumps(data))



def printCommandInvalid(command):
    print(f"Syntax command '{command}' invalid! Please view")
    print(Constants.MESSAGE_SEPARATOR)
    print(Constants.MESSAGE_SYNTAX)