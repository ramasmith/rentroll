
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY","devkey")
    DATABASE = os.environ.get("DATABASE","database.db")
