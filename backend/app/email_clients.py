from __future__ import annotations

import email
import imaplib
import smtplib
from email.mime.text import MIMEText
from typing import List, Dict

from .config import IMAP_HOST, IMAP_USER, IMAP_PASSWORD, IMAP_FOLDER, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


def fetch_support_emails() -> List[Dict[str, str]]:
    filters = ["support", "query", "request", "help"]
    results: List[Dict[str, str]] = []
    if not IMAP_USER or not IMAP_PASSWORD:
        return results
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASSWORD)
    mail.select(IMAP_FOLDER)

    # Search by SUBJECT containing any of the keywords (case-insensitive not supported by IMAP, so OR)
    # We'll fetch recent messages and filter client-side too.
    status, data = mail.search(None, 'ALL')
    if status != 'OK':
        mail.logout()
        return results
    ids = data[0].split()
    for msg_id in ids[-200:]:  # limit to last 200 for efficiency
        status, msg_data = mail.fetch(msg_id, '(RFC822)')
        if status != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg.get('Subject', '') or ''
        sender = email.utils.parseaddr(msg.get('From', ''))[1]
        # Get body (prefer plain)
        body_text = ''
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain' and part.get_content_disposition() != 'attachment':
                    body_text = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                body_text = payload.decode(errors='ignore')
        subj_l = subject.lower()
        if any(k in subj_l for k in filters):
            results.append({
                'sender': sender,
                'subject': subject,
                'body': body_text,
                'received_at': msg.get('Date', ''),
            })
    mail.logout()
    return results


def send_email(to_address: str, subject: str, body: str) -> None:
    if not SMTP_USER or not SMTP_PASSWORD:
        return
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = to_address

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, [to_address], msg.as_string())


