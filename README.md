# ToolSendGmail
Install
sudo apt-get install python3-tk 
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Enabling Gmail API

Detail in: https://www.thepythoncode.com/article/use-gmail-api-in-python

Detail tool
Run on command line with syntax: python main.py [command] [option] [arg]

Detail commands

status - get your status [no option]

login - login gmail
    options:
        -d: default - use account last login to login - no arg
        -n: new - login with new account - no arg
        -c: choose - login with account choosed - has arg
    arg: gmail to login

logout - logout
    options:
        -c: clear - clear cache login - no arg
        -ln: login with new account [only one] - no arg
        -lc: login with account choosed [only one] - has arg
    arg: gmail to login
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

sendmail - send mail
    options:
        -f: file - path file info send mail 