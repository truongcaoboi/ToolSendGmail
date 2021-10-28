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

status - get your status [no option]

login - login gmail
    options:
        -d: default - use account last login to login - no arg
        -n: new - login with new account - no arg
        -c: choose - login with account choosed - has arg

logout - logout
    options:
        -c: clear - clear cache login - no arg
        -ln: login with new account [only one] - no arg
        -lc: login with account choosed [only one] - has arg

listmail - get list your email
    options:
        -mr: maxResults - default is 100 maximum is 500 [has arg]
        -q: querry - Content special to search [has arg]
        -lbs: labelsId - Only return messages with labels that match all of the specified label IDs. [has arg] separator by ','
        -inc: includeSpamTrash - Include messages from SPAM and TRASH in the results. Default False [no arg]

readmail - read email
    no options
    has arg is id of message

markreads - marking email as read
    options:
        -q: querry - Content special to search [has arg]
        -lbs: labelsId - Only return messages with labels that match all of the specified label IDs. [has arg] separator by ','

markreadbyid - marking email as read by id
    no options
    has arg is id of message

markunreads - marking email as unread
    options:
        -q: querry - Content special to search [has arg]
        -lbs: labelsId - Only return messages with labels that match all of the specified label IDs. [has arg] separator by ','

markunreadbyid - marking email as unread by id
    no options
    has arg is id of message

deletemail - delete mail
    options:
        -ids: id messages delete. Ids separator by ","

trashmail - move mail to trash
    options:
        no option
        has args is id message move

untrashmail - remove mail from trash
    options:
        no option
        has args is id message remove

emptytrashmail - remove permanently mail in trash
    no options and args

addlabelmail - add label for mail
    options:
        no options
        has args [ids] [labels] separator by ","

removelabelmail - remove label for mail
    options:
        no options
        has args [ids] [labels] separator by ","

sendmail - send mail
    options:
        -f: file - path file info send mail  support 2 type: html and plain

createdraft - create draft
    options:
        -f: file - path file info send mail

deletedraft - delete draft
    no option
    has args [id] draft remove

deletealldraft - delete all draft
    no option
    no args

readdraft - read draft
    no option
    has args [id] draft read

listdraft - get list draft
    -q: querry
    -mr: maxResults
    -inc: includeSpamTrash

updatedraft - update draft
    -f: file
    has args is id draft update

senddraft - send draft
    no option
    has arg for id draft

createlabel - create label
    options:
        -n: name -- force
        -lv: labelListVisibility - one of ["labelShow","labelShowIfUnread","labelHide", "empty"] default: empty
        -mv: messageListVisibility - one of ["show", "hide", "empty"] default: empty
        -bg: backgroundColor - hex color
        -tc: textColor - hex color

deletelabel - delete label
    has arg for id label

getlabel - get label
    has arg for id label

listlabel - get list label
    no option and arg

patchlabel - patch label
    options:
        -n: name
        -lv: labelListVisibility - one of ["labelShow","labelShowIfUnread","labelHide", "empty"] default: empty
        -mv: messageListVisibility - one of ["show", "hide", "empty"] default: empty
        -bg: backgroundColor - hex color
        -tc: textColor - hex color
    arg is id label

updatelabel - update label
    options:
        -n: name
        -lv: labelListVisibility - one of ["labelShow","labelShowIfUnread","labelHide", "empty"] default: empty
        -mv: messageListVisibility - one of ["show", "hide", "empty"] default: empty
        -bg: backgroundColor - hex color
        -tc: textColor - hex color
    arg is id label
"""
MESSAGE_SEPARATOR = "=" * 50