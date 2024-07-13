from flask import Flask, request, jsonify
from celery import Celery
from datetime import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables
MAIL_ADD = os.getenv('MAIL_ADD')
MAIL_PASS = os.getenv('MAIL_PASS')
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', '/tmp/messaging_system.log')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.example.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Custom logging filter to exclude Werkzeug logs
class ExcludeWerkzeugFilter(logging.Filter):
    def filter(self, record):
        return 'werkzeug' not in record.getMessage()

# Logging setup with specific format
try:
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger()
    logger.addFilter(ExcludeWerkzeugFilter())
    print(f"Logging to {LOG_FILE_PATH}")
except PermissionError as e:
    print(f"Permission error: {e}")
    # Fall back to logging to a different location
    logging.basicConfig(
        filename='/tmp/messaging_system.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    print("Logging to /tmp/messaging_system.log instead")

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email.delay(sendmail)
        logging.info(f"Email queued to {sendmail}")
        return f"Email queued to {sendmail}"

    if talktome:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.info("talktome triggered")
        return "Logged the current time"

    return "Welcome to the Messaging System"

@app.route('/logs')
def get_logs():
    try:
        with open(LOG_FILE_PATH, 'r') as log_file:
            logs = [line.strip() for line in log_file.readlines() if 'werkzeug' not in line]
        return jsonify(logs)
    except Exception as e:
        return str(e), 500

@celery.task
def send_email(to_email):
    msg = MIMEText('This is a test email.')
    msg['Subject'] = 'Test Email'
    msg['From'] = MAIL_ADD
    msg['To'] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(MAIL_ADD, MAIL_PASS)
            server.sendmail(MAIL_ADD, to_email, msg.as_string())
        logging.info(f"Email sent to {to_email}")
        print(f"Email sent to {to_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
