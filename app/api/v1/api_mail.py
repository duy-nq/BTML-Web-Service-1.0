import random
import string
from fastapi import APIRouter
from fastapi_mail import FastMail, MessageSchema
from app.schemas import EmailSchema
from app.core.config import settings

router = APIRouter(tags=['Mail'])

@router.post('/reset-password')
async def send_mail(email: EmailSchema):    
    # 6 digit random password
    reset_password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    template = """
        <html>
            <body>
                <p>Hello,</p>
                <p>Your password has been successfully reset. Here is your new password:</p>
                <p><strong>{}</strong></p>
                <p>We recommend that you change this password to something more memorable as soon as possible.</p>
                <p>If you did not request this password reset or need further assistance, please contact us immediately.</p>
                <p>Thank you!</p>
            </body>
        </html>
        """.format(reset_password)
 
    message = MessageSchema(
        subject="RESET PASSWORD",
        recipients=email.model_dump().get("email"), 
        body=template,
        subtype="html"
    )
 
    fm = FastMail(settings.conf)
    await fm.send_message(message)
    print(message)