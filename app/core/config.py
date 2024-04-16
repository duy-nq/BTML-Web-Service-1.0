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

    SQLALCHEMY_DATABASE_URL = f'mssql+pyodbc://{DEFAULT_USERNAME}:{DEFAULT_PWD}@{SERVER}/{DATABASE}?driver={DRIVER}'

settings = Settings()