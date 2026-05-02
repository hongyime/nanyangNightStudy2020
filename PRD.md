# PRD: nanyangNightStudy2020

## Overview
A Python Flask web app for Nanyang Junior College (NYJC) that lets students register for night study sessions by scanning QR codes via webcam. Features admin login, student check-in via QR code scanning, session time-limiting, and a live video feed. Built with OpenCV and pyzbar for real-time QR decoding. Originally deployed on Heroku.

## Goals
- Live webcam feed served over HTTP for QR code scanning
- Decode student QR codes via pyzbar (zbar library)
- Admin login to manage/view registrations
- Track check-in time and session limits
- Simple authentication via plaintext `login.txt` config
- Display current date/time

## Non-Goals
- Database-backed persistence (appears to use flat files)
- Mobile app
- Cloud QR generation (QR codes generated client-side or external)
- Multi-camera support

## User Stories
- As a student, I want to scan my QR code at the night study counter to check in.
- As an admin, I want to log in to see who has checked in and manage sessions.
- As a teacher on duty, I want to see the live webcam feed to monitor scanning.

## Tech Stack
- **Language**: Python 3.x
- **Framework**: Flask
- **Libraries**: `opencv-python` (cv2), `pyzbar`, `qrcode`, `Pillow`, `gunicorn`
- **Deployment**: Heroku (Procfile), Aptfile for system deps

## Architecture
```
nanyangNightStudy2020/
├── main.py       # Flask app + routes + QR scan logic
├── camera.py     # VideoCamera class — OpenCV webcam frame capture
├── Procfile      # Heroku: web: gunicorn main:app
├── Aptfile       # System packages (libzbar0 for pyzbar)
├── requirements.txt
└── static/
    └── login.txt  # Admin credentials + session config (colon-separated)
```

**Key functions:**
- `gen(camera)` → multipart JPEG stream generator for live video
- `admin_details()` → reads `login.txt` (username:password:start:login:limit)

## Features (detailed)

### Live Video Feed
- `VideoCamera` (camera.py) captures frames via `cv2.VideoCapture(0)`
- `gen()` yields multipart JPEG frames as HTTP streaming response
- Route `/video_feed` returns `Response(gen(camera), mimetype='multipart/form-data')`

### QR Code Scanning
- Each frame decoded with `pyzbar.decode(PIL Image)`
- Decoded data used as student identifier
- Successful scan: logged with timestamp, student ID stored in session/file

### Admin Authentication
- `login.txt` format: `username:password:start_time:login_time:session_limit`
- Admin logs in via `/admin` route; session cookie set on success
- Session fields control who can access the management dashboard

### Session Management
- `start`, `login`, `limit` config values control check-in time window
- Students can only check in within allowed hours
- `placeholder = "NYJC"` — school name shown in UI (configurable)

## Data / Config
| File | Description |
|------|-------------|
| `static/login.txt` | `username:password:start:login:limit` — colon-separated config |

No database — state stored in-memory or flat files during session.

## Deployment / Run
```bash
pip install flask opencv-python pyzbar qrcode Pillow gunicorn
# Linux also requires: apt-get install libzbar0
python main.py  # local dev
gunicorn main:app  # Heroku
```

## Constraints & Notes
- **Camera access**: requires physical webcam; won't work on Heroku/cloud (no camera hardware)
- **plaintext credentials**: `login.txt` stores password in plaintext — not production-safe
- **Heroku Aptfile**: installs `libzbar0` system package for pyzbar
- **Local-only**: meaningful use requires the device to have a connected webcam in the physical check-in location
- **2020 COVID context**: built during period when schools were resuming activities with check-in requirements
