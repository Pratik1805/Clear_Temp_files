import os
import shutil
import tempfile
import stat
import ctypes
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv  # <-- NEW

# Load environment variables
load_dotenv()

LOG_DIR = r"C:\Users\prati\OneDrive\Desktop\Temp_Cleanup_Logs"
LOG_FILE = os.path.join(LOG_DIR, f"temp_cleanup_log_{datetime.date.today()}.log")

def log_message(message):
    """Write logs in log file"""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(message + "\n")

def is_system_or_hidden(file_path):
    try:
        attrs = os.stat(file_path).st_file_attributes
        return bool(attrs & (stat.FILE_ATTRIBUTE_SYSTEM | stat.FILE_ATTRIBUTE_HIDDEN))
    except AttributeError:
        return False

def delete_temp_file(folderPath):
    deleted_items = []
    if not os.path.exists(folderPath):
        log_message(f"! Path not found : {folderPath}")
        return deleted_items
    
    for root, dirs, files in os.walk(folderPath, topdown=False):
        for file in files:
            try:
                file_path = os.path.join(root, file)
                if is_system_or_hidden(file_path):
                    log_message(f"Skipped system/hidden file: {file_path}")
                    continue
                os.remove(file_path)
                deleted_items.append(file_path)
                log_message(f"Deleted file: {file_path}")
            except Exception as e:
                log_message(f"! Could not delete file: {file_path}. \nReason: {e}")

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if os.path.abspath(dir_path) == os.path.abspath(folderPath):
                continue
            try:
                if is_system_or_hidden(dir_path):
                    log_message(f"Skipped system/hidden folder: {dir_path}")
                    continue
                shutil.rmtree(dir_path)
                deleted_items.append(dir_path)
                log_message(f"Deleted folder: {dir_path}")
            except Exception as e:
                log_message(f"! Could not delete folder: {dir_path}.\n Reason: {e}")
    return deleted_items

def clear_windows_temp():
    temp_folders = [
        tempfile.gettempdir(),
        os.path.expandvars(r'%SystemRoot%\Temp'),
    ]
    all_deleted = []
    for folder in temp_folders:
        log_message(f"Clearing contents of {folder}...")
        deleted_files = delete_temp_file(folder)
        all_deleted.extend(deleted_files)
    return all_deleted

def show_acknowledgement(OutputMessage):
    message = OutputMessage
    try:
        ctypes.windll.user32.MessageBoxW(None, message, "Cleanup Complete", 0x40)
    except AttributeError:
        print(message)

def send_email_acknowledgement(deleted_items, recipient_email):
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    subject = "Windows Temp Cleanup Report"
    body = f"""
    Hello,

    The temporary files cleanup has been completed. Below is the summary:

    Total items deleted: {len(deleted_items)}

    Deleted items:
    {', '.join(deleted_items) if deleted_items else 'No items were deleted.'}

    Regards,
    Automated Cleanup Script
    """
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        log_message(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        log_message(f"! Failed to send email. Reason: {e}")

if __name__ == "__main__":
    print("Starting temp file cleanup...")
    log_message("########################## Starting temp file cleanup ##########################")

    deleted_items = clear_windows_temp()

    if deleted_items:
        print("\nCleanup completed!")
        log_message(f"Total items deleted: {len(deleted_items)}")
        log_message("########################## Cleanup Completed ##########################")
        print(f"Log file created at: {LOG_FILE}")

        show_acknowledgement(f"Temporary files cleanup completed.\nLog file saved at:\n{LOG_FILE}")
        send_email_acknowledgement(deleted_items, recipient_email="jsilverhand279@gmail.com")
    else:
        show_acknowledgement("Failed to delete any items.")
        print("\nNo items were deleted.")
        log_message("No items were deleted.")
        log_message("########################## Cleanup Completed ##########################")
        print(f"Log file created at: {LOG_FILE}")
