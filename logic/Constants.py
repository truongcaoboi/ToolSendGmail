SCOPES = [
    'https://mail.google.com/',
    # 'https://www.googleapis.com/auth/gmail.labels',
    # 'https://www.googleapis.com/auth/gmail.send',
    # 'https://www.googleapis.com/auth/gmail.readonly',
    # 'https://www.googleapis.com/auth/gmail.compose',
    # 'https://www.googleapis.com/auth/gmail.insert',
    # 'https://www.googleapis.com/auth/gmail.modify',
    # 'https://www.googleapis.com/auth/gmail.metadata'
]
MY_EMAIL = ''
CLIENT_ID = ''
APPNAME = ""
APPPLICATION_NAME = ""

MESSAGE_SYNTAX = """
syntax: syntax: python main.py [command] [option] [arg]

List command

status - get your status

login - login gmail
    options:
        -d: default - use account last login to login
        -n: new - login with new account
        -c: choose - login with account choosed
    args: gmail to login

logout - logout
    options:
        -c: clear - clear cache
        -ln: login with new account
        -lc: login with account choosed
    args: gmail to login

listmail - get list your email
"""
MESSAGE_SEPARATOR = "=" * 50