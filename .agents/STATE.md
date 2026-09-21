# nanyangNightStudy2020 — Agent State

## Stack
- **Language**: Python
- **Framework**: Flask + OpenCV + pyzbar + gunicorn
- **Dependencies**: cv2, numpy, pyzbar, PIL, flask, gunicorn (see requirements.txt)
- **Type**: Legacy web app — NTU night study room availability checker with QR/camera scanning (2020)

## Last Commit
- **Date**: 2026-09-07 15:21:17 +0000
- **SHA**: 5534b42
- **Message**: chore: sync heartbeat [skip ci]

## Status
- Working tree: untracked `__pycache__/` (not staged, not a concern)
- .agents/: not present (created now)
- AGENTS.md: exists
- Procfile + runtime.txt present (Heroku deployment config)

## Issues Found
- `secret=` match in main.py line 103 is a reCAPTCHA API URL parameter (`checkRecaptcha(response, secretkey)`) — `secretkey` is a function parameter, not a hardcoded value. No live credential.
- __pycache__/ is untracked (should be in .gitignore — minor hygiene)

## Notes
- 2020-era Flask app for NTU night study room availability. Heroku-deployable.
- Treat as archived legacy project.

## Triage Date
2026-09-16
