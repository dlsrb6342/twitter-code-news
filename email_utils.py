from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from credentials import gmail_credential
import smtplib, datetime


def connectSmtp():
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.starttls()
    smtp.ehlo()
    smtp.login(gmail_credential['GMAIL_ID'], gmail_credential['GMAIL_PASSWORD'])
    return smtp


def makeMsg(tweets):
    msg = MIMEMultipart()
    today = datetime.datetime.now()
    msg['Subject'] = f'Tweets. {today.strftime("%A %d. %B %Y")}'
    content = ''
    for tweet in tweets:
        content += f'{tweet["text"]}\n  * tweet url: {tweet["tweet_url"]}\n  * url: {tweet["url"]}'
        content += '\n\n\n'
    text = MIMEText(content)
    print(content)
    msg.attach(text)
    return msg


def sendEmail(smtp, msg):
    with open('./to_addr.txt') as f:
        content = f.readlines()
    to_addr = [x.strip() for x in content]

    for addr in to_addr:
        msg["To"] = addr
        smtp.sendmail(gmail_credential['GMAIL_ID'], addr, msg.as_string())

