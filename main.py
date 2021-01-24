import sys
import os
import json
from urllib.request import *
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

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
hour = now.strftime("%H")
minute = now.strftime("%M")
second = now.strftime("%S")
placeholder =  "NYJC" #can change

''' METHODS'''

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def admin_details():
    with open('static/login.txt', 'r') as f:
        header = f.readline()
        line = f.readline()

    line = line.split(':')
    username = line[0].strip('\n')
    password = line[1].strip('\n')
    start = line[2].strip('\n')
    login = line[3].strip('\n')
    limit = line[4].strip('\n')
    return username,password,start,login,limit

def build_string(limit):
    limit = str(limit)
    string = f'{year}{month}{day}{hour}{minute}{second}{placeholder}{limit}'
    return string

def ord_string(data): # data is string
    if type(data) is str:
        unicode_data = ''
        for letter in data:
            unicode_data += str(ord(letter))
        return unicode_data
    else:
        print('data is not a string')

def hash_unicode(data): # data is a str
    if type(data) is str:
        b_data = bytes(data, 'utf-8') #change to byte
        hash_data = hashlib.sha512(b_data).hexdigest()
        return hash_data
    else:
        print('data is not an integer')

def build_data(hash):
    data = f'{placeholder}{hash}{year}{month}{day}'
    return data

def encode_qr(data):
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=8,)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    logo_display = Image.open('static/nanyang.png')
    logo_display.thumbnail((65, 65))

    logo_pos = ((img.size[0] - logo_display.size[0]) // 2, (img.size[1] - logo_display.size[1]) // 2)
    img.paste(logo_display, logo_pos)

    img.save(f"static/{data}.png")
    with open('static/qrcodes.txt', 'a') as f:
        f.write(data)
        f.write('\n')

def decode_qr(uploaded_file):
    img = decode(Image.open(uploaded_file))
    full_data = img[0][0]
    clean_data = str(full_data, 'utf-8')
    return clean_data

def checkRecaptcha(response, secretkey):
        url = 'https://www.google.com/recaptcha/api/siteverify?'
        url = url + 'secret=' + str(secretkey)
        url = url + '&response=' +str(response)

        jsonobj = json.loads(urlopen(url).read())
        print(jsonobj['success'])
        if jsonobj['success']:
            print(jsonobj['success'])
            return True
        else:
            return False

''' START OF APP '''

app = Flask(__name__, template_folder='templates')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAX_CONTENT_LENGTH'] = 2048 * 2048
app.config['UPLOAD_EXTENSIONS'] = ['.png', ".PNG", '.JPEG', '.JPG', ".jpeg", ".jpg"]
correct_user, correct_pass, start, login, limit = admin_details()

app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LeKpS4aAAAAABrXNs2o5Adx9YGG8RCicK4_sgva'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LeKpS4aAAAAAM_vT-5MLZMBYaNAV8w9TuQUlsbm'
app.config['RECAPTCHA_OPTIONS'] = {'theme':'black'}

RECAPTCHA_PUBLIC_KEY = '6LeKpS4aAAAAABrXNs2o5Adx9YGG8RCicK4_sgva'
RECAPTCHA_PRIVATE_KEY = '6LeKpS4aAAAAAM_vT-5MLZMBYaNAV8w9TuQUlsbm'

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

@app.route('/', methods=["POST",'GET'])
def root():
    with open('static/qrcodes.txt', 'r') as f:
        clean_qrcodes = f.read().splitlines()
    error = f"{len(clean_qrcodes)}/{limit} packages of food redeemed."
    return render_template('generate.html', error=error)

@app.route('/generate', methods=["POST",'GET'])
def generate():
    if request.method == "POST":
        correct_user, correct_pass, start, login, limit = admin_details()
        
        if start == 'False' or int(limit) <= 0:
            return render_template('error.html')
        
        elif start == "True" and int(limit) > 0:
            response = request.form.get('g-recaptcha-response')
            if checkRecaptcha(response, RECAPTCHA_PRIVATE_KEY):
                return redirect(url_for("display"))

            else:
                error = "Captcha failed."
                return render_template('generate.html', error=error)
        else:
            return render_template('error.html')
    else:
        return render_template('error.html')

@app.route('/display', methods=['POST'])
def display():
    correct_user, correct_pass, start, login, limit = admin_details()
    with open('static/qrcodes.txt', 'r') as f:
        clean_qrcodes = f.read().splitlines()
    if start == "True" and int(limit) > 0 and len(clean_qrcodes) < int(limit):
        string = build_string(limit)
        unicode = ord_string(string)
        hash = hash_unicode(unicode)
        data = build_data(hash)
        encode_qr(data)
        filename = data + '.png'
        imagepath = os.path.join(app.root_path, "static", filename)
        print(imagepath)
        return render_template("display.html", filename=filename)
    elif len(clean_qrcodes) >= int(limit):
        return render_template("limit.html")
    else:
        return render_template("error.html")

@app.route('/login', methods=['POST','GET'])
def login():
    
    correct_user, correct_pass, start, login, limit = admin_details()
    login = 'False'
    with open('static/login.txt', 'w') as f:
        f.write("username:password:start:login:limit")
        f.write('\n')
        f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
    
    if request.method == "POST":
        response = request.form.get('g-recaptcha-response')
        if checkRecaptcha(response, RECAPTCHA_PRIVATE_KEY):
            try:
                input_user = request.form['username']
                b_input_user = bytes(str(input_user), 'utf-8') #change to byte
                hash_input_user = hashlib.sha512(b_input_user).hexdigest()

                input_pass = request.form['password']
                b_input_pass = bytes(str(input_pass), 'utf-8') #change to byte
                hash_input_pass = hashlib.sha512(b_input_pass).hexdigest()
            
                if hash_input_user == correct_user and hash_input_pass == correct_pass:
                    with open('static/login.txt', 'w') as f:
                        f.write("username:password:start:login:limit")
                        f.write('\n')
                        login = "True"
                        print(correct_pass)
                        print(correct_user)
                        f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
                    return redirect(url_for("admin"))
                else:
                    error = "Invalid credentials."
                    return render_template("login.html", error=error)
            except:
                error = "Invalid credentials."
                return render_template("login.html", error=error)

        else:
            error = "Captcha failed."
            return render_template("login.html", error=error)
        
    else: #if request is not post
        return render_template("login.html")

@app.route('/admin', methods=['POST','GET'])
def admin():
    correct_user, correct_pass, start, login, limit = admin_details()
    if login == "True":
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))
    
@app.route('/logout', methods=['POST','GET'])
def logout():
    correct_user, correct_pass, start, login, limit = admin_details()
    with open('static/login.txt', 'w') as f:
        f.write("username:password:start:login:limit")
        f.write('\n')
        login = "False"
        f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
    error = "You have logged out successfully."
    return render_template("login.html", error=error)

@app.route('/start', methods=['POST','GET'])
def start():

    correct_user, correct_pass, start, login, limit = admin_details()
    if 'limit' in request.args:
        set_limit = request.args.get("limit")
        if set_limit == '':
            with open('static/login.txt', 'w') as f:
                f.write("username:password:start:login:limit")
                f.write('\n')
                limit = limit
                f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
            error = f"Please input value for limit of QR Codes. Current value is {limit}"
            return render_template("admin.html", error = error)
        elif int(set_limit) > 0:
            set_limit = str(set_limit)
            start = "True"
            with open('static/login.txt', 'w') as f:
                f.write("username:password:start:login:limit")
                f.write('\n')
                f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{set_limit}")
            error = f"You have set limit for QR Codes to be {set_limit}."
            with open('static/qrcodes.txt', 'w') as f:
                pass
            imagepath = os.path.join(app.root_path, "static")
            if os.path.exists(imagepath) == True:
                for name in os.listdir(imagepath):
                    if 'NYJC' in name:
                        path = os.path.join(app.root_path, 'static', name)
                        os.remove(path)
                    else:
                        pass
            return render_template("admin.html", error = error)
    else:
        start = "False"
        with open('static/login.txt', 'w') as f:
            f.write("username:password:start:login:limit")
            f.write('\n')
            f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
        error = "Please input value for limit of QR Codes."
        return render_template("admin.html", error=error)

@app.route('/stop', methods=['POST','GET'])
def stop():
    correct_user, correct_pass, start, login, limit = admin_details()
    if int(limit) > 0 or limit == '':
        with open('static/login.txt', 'w') as f:
            f.write("username:password:start:login:limit")
            f.write('\n')
            start = "False"
            limit = '0'
            f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
        with open('static/qrcodes.txt', 'w') as f:
            pass
        imagepath = os.path.join(app.root_path, "static")
        if os.path.exists(imagepath) == True:
            for name in os.listdir(imagepath):
                if 'NYJC' in name:
                    path = os.path.join(app.root_path, 'static', name)
                    os.remove(path)
                else:
                    pass
        error = f"You have stopped reset limit for QR codes to be 0."
        return render_template("admin.html", error=error)
    else:
        with open('static/qrcodes.txt', 'w') as f:
            pass
        imagepath = os.path.join(app.root_path, "static")
        if os.path.exists(imagepath) == True:
            for name in os.listdir(imagepath):
                if 'NYJC' in name:
                    path = os.path.join(app.root_path, 'static', name)
                    os.remove(path)
                else:
                    pass
        error = f"You have reset the limit for QR codes back to 0."
        return render_template("admin.html", error=error)

@app.route('/scan', methods=['POST','GET'])
def scan():
    correct_user, correct_pass, start, login, limit = admin_details()
    if int(limit) > 0 and start == "True":
        return render_template("scan.html")
    else:
        return render_template("error.html")


@app.route('/upload', methods=['POST','GET'])
def upload():
    correct_user, correct_pass, start, login, limit = admin_details()
    if int(limit) > 0 and start == "True":
        return render_template("upload.html")
    else:
        return render_template("error.html")

@app.route('/verifyQR', methods=['POST','GET'])
def verifyQR():
    print(request.files)
    uploaded_file = request.files['image']
    print(f'uploaded file = {uploaded_file}')
    uploaded = uploaded_file.filename
    if uploaded != '':
        file_ext = os.path.splitext(uploaded)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            error = 'Invalid file extension, only upload PNG or JPEG images.'
            return render_template("upload.html", error=error)
        else:

            with open("static/qrcodes.txt", 'r') as f:
                clean_qrcodes = f.read().splitlines()
                print(f'clean qr = {clean_qrcodes}')
            
            try:
                clean_data = decode_qr(uploaded_file)
                print(f'clean data = {clean_data}')
                print(type(clean_data))
            except:
                error = sys.exc_info()[0]
                return render_template("upload.html", error=error) 

            if type(clean_data) is str:
                try:

                    # 1st check (if file exists in text file)
                    if str(clean_data) in clean_qrcodes:

                        error = "VALID QR."
                        return render_template("upload.html", error=error)
                    else:
                        error = 'INVALID QR1'
                        return render_template("upload.html", error=error)
  
                except:
                    error = sys.exc_info()[0]
                    return render_template("upload.html", error=error) 
            else:
                error = 'INVALID QR3'
                return render_template("upload.html", error=error)
    else:
        error = 'No image uploaded, please try again.'
        return render_template("upload.html", error=error)

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera()),
# 		mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False, threaded=True, use_reloader=True)
