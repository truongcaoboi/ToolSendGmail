# ToolSendGmail
Install

sudo apt-get install python3

sudo apt-get install python3-pip

pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Enabling Gmail API

Detail in: https://www.thepythoncode.com/article/use-gmail-api-in-python

Download and save info creds in to file credentials.json same forder with main.py

Detail tool

Run on command line with syntax: python main.py [command] [arg] [option] [value_option]

Detail commands

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





color.backgroundColor string
The background color represented as hex string #RRGGBB (ex #000000). This field is required in order to set the color of a label. Only the following predefined set of color values are allowed: #000000, #434343, #666666, #999999, #cccccc, #efefef, #f3f3f3, #ffffff, #fb4c2f, #ffad47, #fad165, #16a766, #43d692, #4a86e8, #a479e2, #f691b3, #f6c5be, #ffe6c7, #fef1d1, #b9e4d0, #c6f3de, #c9daf8, #e4d7f5, #fcdee8, #efa093, #ffd6a2, #fce8b3, #89d3b2, #a0eac9, #a4c2f4, #d0bcf1, #fbc8d9, #e66550, #ffbc6b, #fcda83, #44b984, #68dfa9, #6d9eeb, #b694e8, #f7a7c0, #cc3a21, #eaa041, #f2c960, #149e60, #3dc789, #3c78d8, #8e63ce, #e07798, #ac2b16, #cf8933, #d5ae49, #0b804b, #2a9c68, #285bac, #653e9b, #b65775, #822111, #a46a21, #aa8831, #076239, #1a764d, #1c4587, #41236d, #83334c writable


color.textColor string
The text color of the label, represented as hex string. This field is required in order to set the color of a label. Only the following predefined set of color values are allowed: #000000, #434343, #666666, #999999, #cccccc, #efefef, #f3f3f3, #ffffff, #fb4c2f, #ffad47, #fad165, #16a766, #43d692, #4a86e8, #a479e2, #f691b3, #f6c5be, #ffe6c7, #fef1d1, #b9e4d0, #c6f3de, #c9daf8, #e4d7f5, #fcdee8, #efa093, #ffd6a2, #fce8b3, #89d3b2, #a0eac9, #a4c2f4, #d0bcf1, #fbc8d9, #e66550, #ffbc6b, #fcda83, #44b984, #68dfa9, #6d9eeb, #b694e8, #f7a7c0, #cc3a21, #eaa041, #f2c960, #149e60, #3dc789, #3c78d8, #8e63ce, #e07798, #ac2b16, #cf8933, #d5ae49, #0b804b, #2a9c68, #285bac, #653e9b, #b65775, #822111, #a46a21, #aa8831, #076239, #1a764d, #1c4587, #41236d, #83334c


NOTE -f in command sendmail, createdraft, updatedraft

link_default: content_send_mail.json

content_force:

{<br>
    "to":[string],<br>
    "cc":[string],<br>
    "bcc":[string],<br>
    "subject":string,<br>
    "content":string, accept text and link file content (only type 'html')<br>
    "type":"html", choose 'html' if content contain html tag or 'plain' with full text<br>
    "attach":[string]<br>
}

REFERENCE TEMPLATE in folder template