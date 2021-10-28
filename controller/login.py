
from re import T
import controller
from logic.login import login
from logic import Constants

def get_status(argv):
    if(len(argv) > 0):
        printCommandInvalid("status")
        return
    info_system = login.load_infosystem()
    last_login = info_system["last_login"]
    history_login = info_system["history_email"]
    current_login = info_system["current_login"]
    if(len(current_login) == 0):
        print(Constants.MESSAGE_SEPARATOR)
        print("You are not in system")
        print(Constants.MESSAGE_SEPARATOR)
        print("You logined the last time with email: {}".format(last_login))
        print(Constants.MESSAGE_SEPARATOR)
    else:
        print(Constants.MESSAGE_SEPARATOR)
        print("You logined with email: {}".format(current_login))
        print(Constants.MESSAGE_SEPARATOR)
    if(len(history_login) == 0):
        print("You hasn't login system before or you have delete system cache!")
        print(Constants.MESSAGE_SEPARATOR)
    else:
        emails = history_login.split(",")
        print("List your email")
        print(Constants.MESSAGE_SEPARATOR)
        for email in emails:
            print(email)
            print(Constants.MESSAGE_SEPARATOR)

def flogin(argv):
    if(len(argv) == 0):
        option = "-d"
    else:
        option = argv[0]
    info_system = login.load_infosystem()
    if(len(info_system["current_login"]) > 0):
        print("You logged with email {}".format(info_system["current_login"]))
        return
    if(option == "-d" or option == "-n"):
        if(len(argv) > 1):
            printCommandInvalid("login")
            return
        last_login = info_system["last_login"]
        if(option == "-d" and len(last_login) > 0):
            service, data, info_system = login.login(last_login,info_system)
        else:
            service, data, info_system = login.login(info_system=info_system)
        print("Login successfully with email {}".format(data["emailAddress"]))
    elif(option == "-c"):
        if(len(argv) == 2):
            email = argv[1]
            check = False
            for e in info_system["history_email"].split(","):
                if(e == email):
                    check = True
                    break
            if(check):
                service, data, info_system = login.login(email=email,info_system=info_system)
                print("Login successfully with email {}".format(data["emailAddress"]))
            else:
                print(f"Not found email '{email}' in history login system")

        else:
            printCommandInvalid("login")
    else:
        printCommandInvalid("login")

def logout(argv):
    info_system = login.load_infosystem()
    if(len(info_system["current_login"]) == 0):
        print("You had't logined before!")
        return
    if(len(argv) > 0):
        list_op = ["-c", "-ln","-lc"]
        options = []
        args = []
        add_options = True
        has_option_log = False
        check_has = False
        for a in argv:
            if(add_options):
                check_has = False
                for op in list_op:
                    if(op == a):
                        check_has = True
                        if(a == "-ln" or a == "-lc"):
                            if(not has_option_log):
                                has_option_log = True
                            else:
                                printCommandInvalid("logout")
                                return
                        if(a == "-c" and has_option_log):
                            print("You should clear cache before login again with this command!")
                            return
                        options.append(a)
                        if(a == "-c" or a == "-ln"):
                            add_options = True
                        else:
                            add_options = False
                if(not check_has):
                    printCommandInvalid("logout")
                    return
            else:
                args.append(a)
        for option in options:
            if(option == "-c"):
                info_system = login.removeAllCache(info_system)
            elif(option == "-ln"):
                info_system["current_login"] = ""
                service,data, info_system = login.login(email="", info_system=info_system)
            elif(option == "-lc"):
                if(len(args) == 0):
                    printCommandInvalid("logout")
                    return
                else:
                    email = args[0]
                    args = args[1:]
                    check = False
                    for e in info_system["history_email"].split(","):
                        if(e == email):
                            check = True
                            break
                    if(check):
                        service, data , info_system= login.login(email=email,info_system=info_system)
                        print("Login successfully with email {}".format(data["emailAddress"]))
                    else:
                        print(f"Not found email '{email}' in history login system")
            else:
                printCommandInvalid("logout")
                return
    else:
        info_system["current_login"] = ""
        login.save_infosystem(info_system)
    pass

def check_login():
    info_system = login.load_infosystem()
    email =  info_system["current_login"]
    if(email == ""):
        return None, None, None
    else:
        return login.login(email, info_system)

def printCommandInvalid(command):
    print(f"Syntax command '{command}' invalid! Please view")
    print(Constants.MESSAGE_SEPARATOR)
    print(Constants.MESSAGE_SYNTAX)