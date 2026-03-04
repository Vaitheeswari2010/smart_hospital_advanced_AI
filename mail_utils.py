import smtplib
from email.message import EmailMessage
import os

HR_EMAIL = "vaitheeswari02004@gmail.com"   # change later
SENDER_EMAIL = "hospitalgenai@gmail.com"     # gmail
SENDER_PASSWORD = "xmvq afdi ockw hqun"            # gmail app password

def send_resume_to_hr(candidate_name, role, resume_path):
    msg = EmailMessage()
    msg["Subject"] = f"Job Application – {role} | {candidate_name}"
    msg["From"] = SENDER_EMAIL
    msg["To"] = HR_EMAIL

    msg.set_content(f"""
Dear HR Team,

A new job application has been received.

Candidate Name : {candidate_name}
Applied Role   : {role}

Please find the attached resume for review.

Regards,
Sri Durga Hospital Website
""")

    with open(resume_path, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(resume_path)

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="octet-stream",
        filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
