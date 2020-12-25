# from shutil import Error
# from PIL import Image
# from pyzbar.pyzbar import decode
# from pyzbar.pyzbar import decode
# from PIL import Image
# import qrcode
# import time
# from datetime import date, datetime
# import hashlib


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

string = 'helloiambryan'
print(string[-8:])