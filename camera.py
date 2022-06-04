# import the necessary packages
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import sys
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


class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)

    def __del__(self):
        # releasing camera
        self.video.release()

    def get_frame(self):
        while True:
            qrcode = ''
            qrcodes = []
            with open("static/qrcodes.txt", 'r') as f:
                qrcodes.append(f.read().splitlines())
            success, frame = self.video.read()
            for i in decode(frame):
                qrcode += i.data.decode('utf-8')
                print(qrcode)
            if qrcode in qrcodes:
                verification = 'VALID QR'
                myColor = (0, 255, 0)
            else:
                verification = 'INVALID QR'
                myColor = (0, 0, 255)

            pts = np.array([frame.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, myColor, 3)
            pts2 = frame.rect
            cv2.putText(frame, verification,
                        (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, myColor, 2)

            # encode OpenCV raw frame to jpg and displaying it
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
