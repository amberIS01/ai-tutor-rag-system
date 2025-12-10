"""
Email Service Module
Send emails for notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import os
from logger import logger


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(
        self,
        smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        smtp_port: int = int(os.getenv("SMTP_PORT", "587")),
        sender_email: str = os.getenv("SENDER_EMAIL", ""),
        sender_password: str = os.getenv("SENDER_PASSWORD", "")
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html: bool = False
    ) -> bool:
        """Send email"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email
            
            mime_type = "html" if html else "plain"
            message.attach(MIMEText(body, mime_type))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            logger.info(f"Email sent to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_batch_emails(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        html: bool = False
    ) -> int:
        """Send emails to multiple recipients"""
        success_count = 0
        for email in to_emails:
            if self.send_email(email, subject, body, html):
                success_count += 1
        
        return success_count
    
    def send_notification(self, to_email: str, message: str) -> bool:
        """Send notification email"""
        return self.send_email(
            to_email,
            "AI Tutor Notification",
            f"<p>{message}</p>",
            html=True
        )


# Global email service instance
_email_service = None


def get_email_service() -> EmailService:
    """Get email service instance"""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
