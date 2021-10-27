from logic.sendmail.SendMail import SendMail
from logic.login import login
def sendMail(argv):
    info_system = login.load_infosystem()
    service, data, info_system = login.login(info_system["last_login"], info_system)
    factory_send = SendMail(service)
    