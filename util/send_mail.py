import smtplib
from email.mime.text import MIMEText
from email.header import Header
from util import logs_util


class SendMail(object):
    def __init__(self, mail_host):
        self.mail_host = mail_host

    def send(self, title, content, sender, auth_code, receivers):
        message = MIMEText(content, 'html', 'utf-8')
        message['From'] = sender
        message['To'] = ",".join(receivers)
        message['Subject'] = title
        try:
            # smtp_obj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用ssl发信，端口一般是465
            smtp_obj = smtplib.SMTP(self.mail_host, 25)
            smtp_obj.login(sender, auth_code)  # 登录
            smtp_obj.sendmail(sender, receivers, message.as_string())
            print("Mail 发送成功")
            logs_util.logs_util('', "Mail 发送成功", 'info')
        except Exception as e:
            print(e)
            logs_util.logs_util('', e, 'info')


if __name__ == '__main__':
    mail = SendMail('smtp.163.com')
    sender = "fdy19930621@163.com"
    receivers = ['753014306@qq.com', '1285442003@qq.com']
    title = "小滴课堂 邮件测试"
    content = """
    小滴课堂 xdclass.net
    <a href="https://xdclass.net">进入学习更多课程 </a>
     """
    auth_code = "EYABEUMJDKWYOMPL"
    mail.send(title, content, sender, auth_code, receivers)
