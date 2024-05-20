import hashlib

from fastapi_mail import ConnectionConfig

class Settings():
    username = 'sa'
    pwd = '123'
    role = ''
    user_id = ''
    SERVER = 'LAPTOP-S1E2VVUK'
    DATABASE = 'BTML_UPDATE'
    DRIVER = 'ODBC Driver 17 for SQL Server'

    DEFAULT_USERNAME = 'sa'
    DEFAULT_PWD = '123'

    conf = ConnectionConfig(
        MAIL_USERNAME='official.fastservice@gmail.com',
        MAIL_PASSWORD='yfco ahko pofl yxvo',
        MAIL_PORT=587,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        MAIL_FROM='official.fastservice@gmail.com',
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

    SQLALCHEMY_DATABASE_URL = f'mssql+pyodbc://{DEFAULT_USERNAME}:{DEFAULT_PWD}@{SERVER}/{DATABASE}?driver={DRIVER}'

    def sha256_hash(self, password):
        hash = hashlib.sha256(password.encode()).hexdigest()
        return hash

settings = Settings()