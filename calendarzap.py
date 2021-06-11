from flask import Flask, request
from twilio.twiml import messaging_response
import boto3
import os
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import time
import threading
import sys
import datetime
# Twilio credentials and service SID
account_sid = os.environ['twilio_account_sid']
auth_token = os.environ['twilio_auth_token']
client = Client(account_sid, auth_token)


s3 = boto3.resource(
    service_name='s3',
    region_name=os.environ['REGION_NAME'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
)
#
#
app = Flask(__name__)


def daily_reminder(receiver, message):
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='LEMBRETE DIARIO' + '\n\n' + show_datas(),
        to=receiver
    )
    return message
# daily_reminder()


def ler_file_aws():
    # s3.Bucket('calendar-zap').upload_file(Filename='LOG.txt', Key='log.txt')
    # s3.Bucket('calendar-zap').download_file(Key='log.txt', Filename='log.txt')
    # f = open("LOG.txt", "w")
    # f.write("brenoaDASDADSAsASasASAsASasAS\n")
    # f.close()
    # s3.Bucket('calendar-zap').upload_file(Filename='LOG.txt', Key='log.txt')
    return "recebeu"


def check_alrdy_saved(data):
    s3.Bucket('calendar-zap').download_file(Key='log.txt', Filename='log.txt')
    with open("log.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.strip("\n") == data:
                f.close()
                return 1
    f.close()
    # s3.Bucket('calendar-zap').upload_file(Filename='log.txt', Key='log.txt')
    return 0

#


def separate_datas():

    s3.Bucket('calendar-zap').download_file(Key='log.txt', Filename='log.txt')
    dates = []
    i = 0
    with open("log.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if(line.strip("\n") == '.'):
                pass
            else:
                dates.append(line.strip("\n"))
    f.close()

    dates.sort(key=lambda x: datetime.datetime.strptime(
        x.rsplit(None, 2)[0], '%d/%m'))
    word = '\n'.join([str(item) for item in dates]) + '\n'

    f = open("log.txt", "w")
    f.write('.\n' + word)
    f.close()
    s3.Bucket('calendar-zap').upload_file(Filename='log.txt', Key='log.txt')


# s3.Bucket('calendar-zap').upload_file(Filename='log.txt', Key='log.txt')


def write_file(data):
    f = open("log.txt", "a")
    f.write(data)
    f.close()
    # separate_datas()
    s3.Bucket('calendar-zap').upload_file(Filename='log.txt', Key='log.txt')


def show_datas():
    word = ''
    s3.Bucket('calendar-zap').download_file(Key='log.txt', Filename='log.txt')
    with open('log.txt') as f:
        line = f.readline()
        while line:
            line = f.readline()
            word += line
    return word


def del_data(word):
    delet = 0
    s3.Bucket('calendar-zap').download_file(Key='log.txt', Filename='log.txt')
    with open("log.txt", "r") as f:
        lines = f.readlines()
        with open("log.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != word:
                    f.write(line)
                else:
                    delet = 1
    f.close()
    s3.Bucket('calendar-zap').upload_file(Filename='log.txt', Key='log.txt')
    return delet


def del_all():
    f = open("log.txt", "w")
    f.write("." + "\n")
    f.close()
    s3.Bucket('calendar-zap').upload_file(Filename='log.txt', Key='log.txt')


@ app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if(incoming_msg.count(" ") > 3):
        quote = '_Insira no máx. até 2 argumentos + "."_'
        msg.body(quote)
        responded = True
        return str(resp)
    if 'salvar' in incoming_msg or 'save' in incoming_msg:
        ler_file_aws()
        if(incoming_msg.find('/') == 9):
            data = incoming_msg[(incoming_msg.find('/'))-2:incoming_msg.find('/')+3] + \
                incoming_msg[incoming_msg.find('/')+3:incoming_msg.find('.')]
            responded = True
            if(check_alrdy_saved(data)):
                quote = '_data já foi gravada_'
                msg.body(quote)
                responded = True
            else:
                palavra = data + "\n"
                write_file(palavra)
                separate_datas()
                quote = '*salvo!*'
                msg.body(quote)
                responded = True
        else:
            quote = '*formato inválido*'
            msg.body(quote)
            responded = True

    elif 'datas' in incoming_msg or 'show' in incoming_msg:
        word = show_datas()
        if word == 1:
            quote = '_Nenhuma data foi salva_'
            msg.body(quote)
            responded = True
        msg.body(word)
        responded = True
    elif 'del' in incoming_msg:
        word = incoming_msg[(incoming_msg.find('l')+2):(incoming_msg.find('.'))]
        delet = del_data(word)
        if delet == 1:
            quote = '*deletado!*'
            msg.body(quote)
            responded = True
        else:
            quote = '_data não encontrada_'
            msg.body(quote)
            responded = True
    elif 'exc tudo' in incoming_msg:
        del_all()
        quote = '*datas deletadas*'
        msg.body(quote)
        responded = True

    # if 'datas' in incoming_msg:
        # word = read_file()
    if not responded:
        msg.body('_comando inválido, digite: help_')
    return str(resp)


#
if __name__ == '__main__':
    # daily_reminder()
    app.config['DEBUG'] = True
    app.run()
