import sys, os
from typing import ChainMap
from controller import *
from controller import *
from controller import login, boxmail, sendmail, draftC as draft, label
from logic import Constants


def table_controller(service, info_system, command, argv):
    if(command == "listmail"):
        boxmail.search_messages(service, info_system, argv, command)
    elif(command == "readmail"):
        boxmail.read_message(service, info_system, argv, command)
    elif(command == "markreads"):
        boxmail.mark_as_read(service, info_system, argv, command)
    elif(command == "markreadbyid"):
        boxmail.mark_as_read_byid(service, info_system, argv, command)
    elif(command == "markunreads"):
        boxmail.mark_as_unread(service, info_system, argv, command)
    elif(command == "markunreadbyid"):
        boxmail.mark_as_unread_byid(service, info_system, argv, command)
    elif(command == "sendmail"):
        sendmail.sendMail(service, info_system, argv, command)
    elif(command == "deletemail"):
        boxmail.delete_messages(service, info_system, argv, command)
    elif(command == "trashmail"):
        boxmail.trash(service, info_system, argv, command)
    elif(command == "untrashmail"):
        boxmail.untrash(service,info_system, argv, command)
    elif(command == "emptytrashmail"):
        boxmail.emptytrash(service, info_system, argv, command)
    elif(command == "addlabelmail"):
        boxmail.addLabels(service, info_system, argv, command)
    elif(command == "removelabelmail"):
        boxmail.removeLabels(service, info_system, argv, command)
    elif(command == "createdraft"):
        draft.create(service, info_system, argv, command)
    elif(command == "deletedraft"):
        draft.delete(service, info_system, argv, command)
    elif(command == "deletealldraft"):
        draft.deleteAll(service, info_system, argv, command)
    elif(command == "readdraft"):
        draft.read(service, info_system, argv, command)
    elif(command == "listdraft"):
        draft.search(service, info_system, argv, command)
    elif(command == "updatedraft"):
        draft.update(service, info_system, argv, command)
    elif(command == "senddraft"):
        draft.send(service, info_system, argv, command)
    elif(command == "createlabel"):
        label.create(service, info_system, argv, command)
    elif(command == "deletelabel"):
        label.delete(service, info_system, argv, command)
    elif(command == "getlabel"):
        label.get(service, info_system, argv, command)
    elif(command == "listlabel"):
        label.search(service, info_system, argv, command)
    elif(command == "patchlabel"):
        label.patch(service, info_system, argv, command)
    elif(command == "updatelabel"):
        label.update(service, info_system, argv, command)
    else:
        print("Not found command!")


if __name__ == "__main__":
    if(len(sys.argv)<2):
        print("Syntax error! Please view")
        print(Constants.MESSAGE_SEPARATOR)
        print(Constants.MESSAGE_SYNTAX)
    else:
        command = sys.argv[1]
        if(command == "status"):
            login.get_status(sys.argv[2:])
        elif(command == "login"):
            login.flogin(sys.argv[2:])
        elif(command == "logout"):
            login.logout(sys.argv[2:])
        elif(command == "help"):
            print(Constants.MESSAGE_SYNTAX)
        else:
            service, data, info_system = login.check_login()
            if(service == None):
                print("You must login before!")
            else:
                table_controller(service, info_system, command, sys.argv[2:])
