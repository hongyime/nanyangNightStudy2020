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
import time
from datetime import datetime
import hashlib

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
hour = now.strftime("%H")
minute = now.strftime("%M")
second = now.strftime("%S")
placeholder =  "NYJC" #can change

''' METHODS'''

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
    data = f'{placeholder}{hash}{year}{month}{day}' # always check last 8 digits agaist current date
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

def decode_qr(data):
    img = decode(Image.open(f'static/{data}.png'))
    full_data = img[0][0]
    clean_data = str(full_data, 'utf-8')
    print(clean_data)
    return clean_data

''' START OF APP '''

app = Flask(__name__, template_folder='templates') 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['MAX_CONTENT_LENGTH'] = 2048 * 2048
app.config['UPLOAD_EXTENSIONS'] = ['.png', ".PNG", '.JPEG', '.JPG', ".jpeg", ".jpg"]
correct_user, correct_pass, start, login, limit = admin_details()
print(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")

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

@app.route('/', methods=['POST','GET'])
def root():
    correct_user, correct_pass, start, login, limit = admin_details()
    print(type(start))
    if start == 'False':
        return render_template('error.html')
    elif start == "True":
        imagepath = os.path.join(app.root_path, "static")
        app_path = os.path.join(app.root_path)
        if os.path.exists(imagepath) == True:
            for name in os.listdir(imagepath):
                if 'NYJC' in name:
                    path = os.path.join(app.root_path, 'static', name)
                    os.remove(path)
                else:
                    pass
        return render_template('generate.html')
    else:
        return render_template('error.html')

@app.route('/display', methods=['POST','GET'])
def display():
    string = build_string(limit)
    unicode = ord_string(string)
    hash = hash_unicode(unicode)
    data = build_data(hash)
    encode_qr(data)
    filename = data + '.png'
    imagepath = os.path.join(app.root_path, "static", filename)
    print(imagepath)
    app_path = os.path.join(app.root_path)
    return render_template("display.html", filename=filename)

@app.route('/login', methods=['POST','GET'])
def login():
    login = 'False'
    with open('static/login.txt', 'w') as f:
        f.write("username:password:start:login:limit")
        f.write('\n')
        f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
    error = "Please input correct username and password."
    return render_template("login.html", error=error)

@app.route('/verify', methods=['POST','GET'])
def verify():
    correct_user, correct_pass, start, login, limit = admin_details()
    if 'username' and 'password' in request.args:
        username = request.args.get("username")
        password = request.args.get("password")
        print(username)
        print(password)
        if username == correct_user and password == correct_pass:
            with open('static/login.txt', 'w') as f:
                f.write("username:password:start:login:limit")
                f.write('\n')
                login = "True"
                print(correct_pass)
                print(correct_user)
                f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
            return render_template("admin.html")
        else:
            return redirect('/login')
    else:
        return redirect('/login')

@app.route('/admin', methods=['POST','GET'])
def admin():
    correct_user, correct_pass, start, login, limit = admin_details()
    # if login == "True":
    #     return redirect('/login')
    
    return render_template("admin.html")

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
        limit = request.args.get("limit")
        print(limit)
        limit = str(limit)
        start = "True"
        with open('static/login.txt', 'w') as f:
            f.write("username:password:start:login:limit")
            f.write('\n')
            f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
        error = f"You have set limit for QR codes to be {limit}"
        return render_template("admin.html", error = error)
    else:
        return redirect("/admin")

@app.route('/stop', methods=['POST','GET'])
def stop():
    correct_user, correct_pass, start, login, limit = admin_details()
    if int(limit) > 0:
        with open('static/login.txt', 'w') as f:
            f.write("username:password:start:login:limit")
            f.write('\n')
            start = "False"
            limit = '0'
            f.write(f"{correct_user}:{correct_pass}:{start}:{login}:{limit}")
        return render_template("admin.html")
    else:
        return redirect("/admin")

if __name__ == '__main__':
    app.run(debug=False, threaded=True, use_reloader=True)