from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type  

import os
class SendMail:
    def __init__(self, service) -> None:
        self.service = service


    def add_attachment(self, message, filename):
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    def build_message(self, destination, email_send,cc, bcc, obj, body, attachments=[]):
        if not attachments: # no attachments given
            message = MIMEText(body)
        else:
            message = MIMEMultipart()
            message.attach(MIMEText(body))
            for filename in attachments:
                self.add_attachment(message, filename)
        message['to'] = destination
        message['from'] = email_send
        if(len(cc) > 0):
            message['cc'] = cc
        if(len(bcc) > 0):
            message['bcc'] = bcc
        message['subject'] = obj
        return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}
    
    def send_message(self,user_id, destination, email_send,cc='', bcc='', obj='', body='', attachments=[]):
        return self.service.users().messages().send(
        userId=user_id,
        body=self.build_message(destination,email_send,cc,bcc, obj, body, attachments)
        ).execute()