from shutil import Error
from PIL import Image
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import time
from datetime import date, datetime
import hashlib
import sys
import os
from PIL import Image
import time
from flask import Flask, render_template, request, redirect
from flask import *
from flask import send_file, send_from_directory, safe_join, abort
from main import app
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import cv2
import time
from datetime import datetime
import hashlib
from camera import VideoCamera
import base64
import numpy as np
import imutils
from io import StringIO
import io

# data = 'admin'
# b_data = bytes(data, 'utf-8') #change to byte
# hash_data = hashlib.sha512(b_data).hexdigest()
# print(hash_data)

# now = datetime.now()
# year = now.strftime("%Y")
# month = now.strftime("%m")
# day = now.strftime("%d")
# hour = now.strftime("%H")
# minute = now.strftime("%M")
# second = now.strftime("%S")
# placeholder =  "NYJC" #can change

# def build_string(limit):
#     limit = str(limit)
#     string = f'{year}{month}{day}{hour}{minute}{second}{placeholder}{limit}'
#     return string

# def ord_string(data): # data is string
#     if type(data) is str:
#         unicode_data = ''
#         for letter in data:
#             unicode_data += str(ord(letter))
#         return unicode_data
#     else:
#         print('data is not a string')

# def hash_unicode(data): # data is a str
#     if type(data) is str:
#         b_data = bytes(data, 'utf-8') #change to byte
#         hash_data = hashlib.sha512(b_data).hexdigest()
#         return hash_data
#     else:
#         print('data is not an integer')

# def build_data(hash):
#     data = f'{placeholder}{hash}{year}{month}{day}' # always check last 8 digits agaist current date
#     return data

# def encode_qr(data):
#     qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=8,)
#     qr.add_data(data)
#     qr.make(fit=True)

#     img = qr.make_image(fill_color="black", back_color="white")

#     logo_display = Image.open('static/nanyang.png')
#     logo_display.thumbnail((65, 65))

#     logo_pos = ((img.size[0] - logo_display.size[0]) // 2, (img.size[1] - logo_display.size[1]) // 2)
#     img.paste(logo_display, logo_pos)

#     img.save(f"static/{data}.png")
#     with open('static/qrcodes.txt', 'a') as f:
#         f.write(data)
#         f.write('\n')

# def decode_qr(data):
#     img = decode(Image.open(f'static/{data}.png'))
#     full_data = img[0][0]
#     clean_data = str(full_data, 'utf-8')
#     print(clean_data)
#     return clean_data


# string = build_string(100)
# unicode = ord_string(string)
# hash = hash_unicode(unicode)
# data = build_data(hash)
# encode_qr(data)
# print(decode_qr(data))

# def admin_details():
#     with open('static/login.txt', 'r') as f:
#         header = f.readline()
#         line = f.readline()

#     line = line.split(':')
#     username = line[0]
#     password = line[1]
#     check = line[2]

#     return username,password,check

# username,password,check = admin_details()
# print(f'{username},{password}')

# string = 'helloiambryan'
# print(string[-8:])


from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    # converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
