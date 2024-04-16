class Settings():
    USERNAME = 'sa'
    PWD = '123'
    SERVER = 'LAPTOP-S1E2VVUK'
    DATABASE = 'BTML'
    DRIVER = 'ODBC Driver 17 for SQL Server'

    SQLALCHEMY_DATABASE_URL = f'mssql+pyodbc://{USERNAME}:{PWD}@{SERVER}/{DATABASE}?driver={DRIVER}'

settings = Settings()