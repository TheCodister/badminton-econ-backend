class Config:
    SECRET_KEY = 'BenCuber@2002'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:BenCuber%402601@localhost/badminton'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'BenCuber@2002'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
