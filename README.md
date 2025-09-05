# ClearTemp - Windows Temporary File Cleanup Script

## Overview

ClearTemp is a Python script designed to automate the cleanup of temporary files and folders on a Windows system. It helps free up disk space by removing unnecessary files from system-defined temporary directories. The script also provides logging, user notifications, and email reporting for a complete cleanup experience.

## Features

- **Temporary File Cleanup**: Deletes files and folders from system-defined temporary directories.
- **Logging**: Logs all actions, including deleted files, skipped files, and errors, to a log file.
- **Acknowledgement**: Displays a message box to notify the user upon completion of the cleanup process.
- **Email Notification**: Sends an email report summarizing the cleanup.

## Prerequisites

- Python 3.12 or higher
- Required Python packages:
  - `python-dotenv`
  - `smtplib`
- A `.env` file with the following variables:
  ```env
  EMAIL_ADDRESS=your_email@example.com
  EMAIL_PASSWORD=your_email_password
