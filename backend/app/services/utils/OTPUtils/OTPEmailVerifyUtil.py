import random
import smtplib
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.app.core.config import SMTP_PASSWORD, SMTP_USERNAME



class RateLimitError(Exception):
    pass


class OTPUtils:
    def __init__(self):
        self.sender = SMTP_USERNAME
        self.password = SMTP_PASSWORD
        self._email_timestamps = {}
        self._rate_limit_duration = timedelta(minutes=2)  # 2 minutes between emails

    def _check_rate_limit(self, email):
        current_time = datetime.now()
        if email in self._email_timestamps:
            time_diff = current_time - self._email_timestamps[email]
            if time_diff < self._rate_limit_duration:
                remaining_seconds = int((self._rate_limit_duration - time_diff).total_seconds())
                raise RateLimitError(f"Please wait {remaining_seconds} seconds before requesting another OTP")
        self._email_timestamps[email] = current_time

    def send_email(self, otp, recipients):
        try:
            for recipient in recipients:
                self._check_rate_limit(recipient)
            html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xác Thực OTP - Meowmo</title>
</head>
<body style="background-color: #f0f2f5; margin: 0; padding: 0; font-family: Arial, sans-serif;">
    <table cellpadding="0" cellspacing="0" width="100%" style="max-width: 400px; margin: 50px auto;">
        <tr>
            <td>
                <table cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border-radius: 10px; border: 1px solid rgba(243, 116, 41, 0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="background-color: #F37429; padding: 25px; color: #ffffff; font-size: 26px; font-weight: bold; text-align: center; border-radius: 10px 10px 0 0;">
                            Xác Thực OTP Meowmo
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px; text-align: center; background-color: #ffffff;">
                            <h1 style="color: #2c3e50; font-size: 28px; margin-bottom: 30px; text-shadow: 0 1px 1px rgba(0,0,0,0.05);">Mã Xác Thực (OTP) Của Bạn</h1>
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin: 20px 0;">
                                <tr>
                                    <td style="text-align: center;">
                                        <div style="display: inline-block; font-size: 36px; font-weight: bold; color: #F37429; background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%); padding: 15px 30px; border: 2px solid #F37429; border-radius: 12px; min-width: 120px; text-align: center; margin: 0; box-shadow: 0 2px 4px rgba(243,116,41,0.1), inset 0 1px 0 rgba(255,255,255,0.9); letter-spacing: 4px;">{''.join(otp)}</div>
                                    </td>
                                </tr>
                            </table>
                            <p style="font-size: 16px; color: #34495e; line-height: 1.6; margin-bottom: 30px; text-shadow: 0 1px 0 rgba(255,255,255,0.8);">
                                Vui lòng sử dụng mã OTP này để hoàn tất xác thực. Mã OTP có hiệu lực trong vòng 10 phút.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px 20px; text-align: center; border-radius: 0 0 10px 10px; border-top: 1px solid rgba(243,116,41,0.1);">
                            <p style="font-size: 28px; font-weight: bold; color: #F37429; margin: 0;">Gửi bởi Meowmo</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
            msg = MIMEText(html_content, 'html')
            msg['Subject'] = "[Meowmo] Mã Xác Thực OTP"
            msg['From'] = f"Meowmo <{self.sender}>"
            msg['To'] = ', '.join(recipients)

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(self.sender, self.password)
            s.sendmail(self.sender, recipients, msg.as_string())
            s.quit()
        except RateLimitError as e:
            raise RateLimitError(str(e))

    def send_email_reset_password(self, otp, recipients):
        try:
            for recipient in recipients:
                self._check_rate_limit(recipient)
            html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Xác Thực OTP - Meowmo</title>
</head>
<body style="background-color: #f0f2f5; margin: 0; padding: 0; font-family: Arial, sans-serif;">
    <table cellpadding="0" cellspacing="0" width="100%" style="max-width: 400px; margin: 50px auto;">
        <tr>
            <td>
                <table cellpadding="0" cellspacing="0" width="100%" style="background-color: #ffffff; border-radius: 10px; border: 1px solid rgba(243, 116, 41, 0.2); box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
                    <tr>
                        <td style="background-color: #F37429; padding: 25px; color: #ffffff; font-size: 26px; font-weight: bold; text-align: center; border-radius: 10px 10px 0 0;">
                            Xác Thực OTP Meowmo
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 40px; text-align: center; background-color: #ffffff;">
                            <h1 style="color: #2c3e50; font-size: 28px; margin-bottom: 30px; text-shadow: 0 1px 1px rgba(0,0,0,0.05);">Mã Xác Thực (OTP) Của Bạn</h1>
                            <table cellpadding="0" cellspacing="0" width="100%" style="margin: 20px 0;">
                                <tr>
                                    <td style="text-align: center;">
                                        <div style="display: inline-block; font-size: 36px; font-weight: bold; color: #F37429; background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 100%); padding: 15px 30px; border: 2px solid #F37429; border-radius: 12px; min-width: 120px; text-align: center; margin: 0; box-shadow: 0 2px 4px rgba(243,116,41,0.1), inset 0 1px 0 rgba(255,255,255,0.9); letter-spacing: 4px;">{''.join(otp)}</div>
                                    </td>
                                </tr>
                            </table>
                            <p style="font-size: 16px; color: #34495e; line-height: 1.6; margin-bottom: 30px; text-shadow: 0 1px 0 rgba(255,255,255,0.8);">
                                Vui lòng sử dụng mã OTP này để hoàn tất xác thực. Mã OTP có hiệu lực trong vòng 10 phút.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px 20px; text-align: center; border-radius: 0 0 10px 10px; border-top: 1px solid rgba(243,116,41,0.1);">
                            <p style="font-size: 28px; font-weight: bold; color: #F37429; margin: 0;">Gửi bởi Meowmo</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
            msg = MIMEText(html_content, 'html')
            msg['Subject'] = "[Meowmo] OTP Đặt Lại Mật Khẩu"
            msg['From'] = f"Meowmo <{self.sender}>"
            msg['To'] = ', '.join(recipients)

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(self.sender, self.password)
            s.sendmail(self.sender, recipients, msg.as_string())
            s.quit()
        except RateLimitError as e:
            raise RateLimitError(str(e))

    @staticmethod
    def GenerateOTP():
        otp = str(random.randint(100000, 999999))
        return otp


class SendEmail:
    def __init__(self):

        self.sender = SMTP_USERNAME
        self.password = SMTP_PASSWORD

    def send_meeting_note_to_email(self, email, note: str):
        # Create the email message

        msg = MIMEMultipart()
        msg['From'] = f"Meowmo <{self.sender}>"
        msg['To'] = email
        msg['Subject'] = "Meeting Note"

        # Attach the meeting note as plain text
        # Attach the meeting note as HTML content
        html_content = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Meeting Note by Meowmo</title>
        </head>
        <body style="background-color: #f0f2f5; margin: 0; padding: 0; font-family: Arial, sans-serif;">
            <div style="width: 100%; max-width: 400px; margin: 50px auto; background-color: #fff; box-shadow: 0px 15px 25px rgba(0,0,0,0.1); border-radius: 10px; overflow: hidden;">
                <div style="background-color: #007bff; padding: 25px; color: #fff; font-size: 26px; font-weight: bold; text-align: center; letter-spacing: 1px;">
                    Meeting Note by Meowmo
                </div>
                <div style="padding: 40px; text-align: center;">
                    <h1 style="color: #333; font-size: 24px; margin-bottom: 20px;">Ghi chú cuộc hợp gần đây của bạn</h1>
                    <p style="font-size: 16px; color: #666; margin-bottom: 30px;">Hãy tải về và sử dụng</p>
                </div>
                <div style="background-color: #f7f7f7; padding: 20px; text-align: center;">
                    <p style="font-size: 16px; font-weight: bold; color: #d9534f; margin: 0;">Sent by Meowmo</p>
                    <div style="margin-top: 10px;">
                        <a href="https://www.facebook.com/profile.php?id=61564246875319" style="display: inline-block; margin: 0 10px;"><svg style="width: 24px; opacity: 0.8;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 512"><path d="M279.1 288l14.2-92.7h-88.9v-60.1c0-25.4 12.4-50.1 52.2-50.1h40.4V6.3S260.4 0 225.4 0c-73.2 0-121.1 44.4-121.1 124.7v70.6H22.9V288h81.4v224h100.2V288z"/></svg></a>
                        <a href="https://www.linkedin.com/company/fpt-telecom-hcm" style="display: inline-block; margin: 0 10px;"><svg style="width: 24px; opacity: 0.8;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 512"><path d="M100.3 448H7.4V148.9h92.9zM53.8 108.1C24.1 108.1 0 83.5 0 53.8a53.8 53.8 0 0 1 107.6 0c0 29.7-24.1 54.3-53.8 54.3zM447.9 448h-92.7V302.4c0-34.7-.7-79.2-48.3-79.2-48.3 0-55.7 37.7-55.7 76.7V448h-92.8V148.9h89.1v40.8h1.3c12.4-23.5 42.7-48.3 87.9-48.3 94 0 111.3 61.9 111.3 142.3V448z"/></svg></a>
                    </div>
                </div>
            </div>
        </body>
        </html>"""
        msg.attach(MIMEText(html_content, 'html'))
        # Attach the meeting note file
        filename = "meeting_note.txt"
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(note.encode('utf-8'))
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f"attachment; filename={filename}")
        msg.attach(attachment)

        # Send the email
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(self.sender, self.password)
        s.sendmail(self.sender, email, msg.as_string())
        s.quit()
