import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, Dict
import json

def load_smtp_from_config():
    def decorator(send_email):
        def wrapper(to_email: str , subject: str , body: str):
            with open("./config/email.json" , encoding='utf-8') as config_file:
                config =  json.load(config_file)
            smtp_info = config["smtp"]
            mail_info = {
                'from_email': smtp_info['user'],
                'to_email': to_email,
                'subject': subject,
                'body': body
            }
            return send_email(smtp_info=smtp_info , mail_info=mail_info)
        return wrapper
    return decorator
pass

@load_smtp_from_config()
def send_email(smtp_info: Dict[str , Union[str , int]] , mail_info: Dict[str , str]):
    # copy value
    from_email = mail_info['from_email']
    to_email = mail_info['to_email']
    subject = mail_info['subject']
    body = mail_info['body']

    # 创建MIMEMultipart对象，发送人、收件人、标题、正文由mail_info字典变量传递
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 连接到SMTP服务器并发送邮件
    # 初始化server变量
    server = None
    # 连接到SMTP服务器并发送邮件
    try:
        smtp_send(smtp_info , mail_info , msg)
        print("Email sent successfully.")
    except smtplib.SMTPServerDisconnected as e:
        print(f"SMTP server disconnected: {e}")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
    finally:
        # 只有在server已连接且未断开时才调用quit()
        if server and server.sock:
            try:
                server.quit()
            except smtplib.SMTPServerDisconnected:
                print("Server already disconnected, cannot quit.")



def smtp_send(smtp_info: Dict[str , Union[str , int]] , mail_info: Dict[str , str] , msg: MIMEMultipart):
    # copy value
    from_email = mail_info['from_email']
    to_email = mail_info['to_email']
    smtp_server = smtp_info['server']
    smtp_port = smtp_info['port']
    smtp_user = smtp_info['user']
    smtp_password = smtp_info['password']
    smtp_type = smtp_info['type']

    if smtp_type == 'ssl':
        # ssl发送
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
    elif smtp_type == 'tls':
        # tls发送
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 开启TLS加密
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())
    else :
        print('发送加密类型不是ssl或tls中的任意一种')
        raise smtplib.SMTPException
