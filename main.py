import sys, os
from controller import *
from controller import *
from controller import login, boxmail, sendmail
from logic import Constants
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
        elif(command == "listmail"):
            boxmail.search_messages(sys.argv[2:])
        elif(command == "readmail"):
            boxmail.read_message(sys.argv[2:])
        elif(command == "markreads"):
            boxmail.mark_as_read(sys.argv[2:])
        elif(command == "markreadbyid"):
            boxmail.mark_as_read_byid(sys.argv[2:])
        elif(command == "markunreads"):
            boxmail.mark_as_unread(sys.argv[2:])
        elif(command == "markunreadbyid"):
            boxmail.mark_as_unread_byid(sys.argv[2:])
        else:
            print("Not found command!")