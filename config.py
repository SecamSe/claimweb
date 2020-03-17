class Config:
    DEBUG = True
    ENV = "Se"
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:root@postgres/claimweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
