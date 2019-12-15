import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


#Формирование письма для отправки на почту
def send_mail(address,url,result):
    body = MIMEText(f'Result: url = {url}, hash_sum = {result}')
    message = MIMEMultipart()
    message['From'] = 'example_address@mail.ru'                          
    message['To'] = address                            
    message['Subject'] = '[no spam]'
    message.attach(body)
    mail = smtplib.SMTP('smtp.mail.ru',587)
    mail.starttls()
    mail.login('example_address@mail.ru','example_password')
    mail.sendmail('example_address@mail.ru',address,message.as_string())
    mail.close()