from pydoc import doc
from urllib import response
from xml.dom.minidom import Document
from flask import Flask, request
import requests, json
import sqlite3
import os
from sklearn.utils import resample



def get_file(file_id, file_name, chat_id):
    method = "getFile"

    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"file_id": file_id}
    req = requests.post(url, data=data)
    r = req.json()
    file_path = r["result"]["file_path"]
    download_file(file_path, file_name, str(chat_id))

def download_file(file_path, file_name, chat_id):
    url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    #data = {"file_id": file_id}
    if not os.path.exists('downloads/' + chat_id):
        os.mkdir('downloads/' + chat_id)
    req = requests.get(url)
    open('downloads/' + chat_id + '/' + file_name, "wb").write(req.content)

def send_message(chat_id, text):
    method = "sendMessage"

    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def send_document(chat_id, document):
    method = "sendDocument"

    url = f"https://api.telegram.org/bot{token}/{method}"
    chat_id_file = str(chat_id)
    file_path = 'downloads/' + chat_id_file + '/' + document
    f = open(file_path, 'rb')
    f_bytes = f.read()
    f.close
    params = ['document']
    ynivar = (document, f_bytes)
    data = {"chat_id": chat_id}
    r = requests.post(url, data=data, files={'document' : (document, f_bytes)})
    #print(r.json)
    print(r)

def button1(chat_id):
    chat_id = str(chat_id)
    list_of_files = os.listdir('downloads/' + chat_id)
    list_of_filenames = []
    for file in list_of_files:
        filename = [{
        "text": "FILE:" + file
        #"request_contact":True,
        
        }]
        print(filename)
        list_of_filenames.append(filename)
        


    method = "sendMessage"
    
    #reply_markup={"KeyboardButton":["text":"fff", "one_time_keyboard":True]}
    url = f"https://api.telegram.org/bot{token}/{method}"


    data = {"chat_id": chat_id, "text": "Ваши Файлы", "reply_markup": json.dumps({"keyboard": 
    list_of_filenames
    , "one_time_keyboard":True})}

    requests.post(url, data=data)


app = Flask(__name__)
token = "5321950119:AAHkTOtSNCD_-2c2cwVxBQf4Q3MvwCPHy0M"
@app.route("/", methods=["POST"])
async def receive_update():

    r = request.json
    print(r)
    if 'contact' in r['message']:
        chat_id = r['message']['chat']['id']
        phone = r['message']['contact']['phone_number']
        print(r['message']['contact']['phone_number'])
        send_message(chat_id, phone)
        return {"ok": True}

    if 'document' in r['message']:
        chat_id = r['message']['chat']['id']
        file_id = r['message']['document']['file_id']
        file_name = r['message']['document']['file_name']
        get_file(file_id, file_name, chat_id)
        #print(file_id)
        #chat_id = r['message']['chat']['id']
        #phone = r['message']['contact']['phone_number']
        #print(r['message']['contact']['phone_number'])
        #send_message(chat_id, phone)
        return {"ok": True}
    
    chat_id = r['message']['chat']['id']
    text = r['message']['text']
    if text == "/start":
        button1(chat_id)
        #print(r)
        return {"ok": True}

    if "FILE:" in text: 
        
        filename = text.replace("FILE:", '')
        print(filename)
        send_document(chat_id, filename)
        return {"ok": True}
        

if __name__ == '__main__':
    app.run(host='0.0.0.0')