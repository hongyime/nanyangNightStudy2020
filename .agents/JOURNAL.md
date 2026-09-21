# nanyangNightStudy2020 — Agent Journal

## 2026-09-16 — Baseline Wave 2d Triage

- Ran baseline triage as part of wave2d legacy repo audit
- Stack: Python Flask web app (OpenCV, pyzbar, gunicorn — NTU night study room checker)
- Last commit: 2026-09-07 (CI/config only; code is 2020-era)
- Working tree has untracked __pycache__/ (minor hygiene, not a risk)
- secret= match in main.py is reCAPTCHA URL param construction — secretkey is a function parameter, not hardcoded
- Heroku Procfile + runtime.txt present
- Treat as archived legacy project
- No action required
