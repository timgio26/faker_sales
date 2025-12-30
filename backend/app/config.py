import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR,'instance',"app.db")

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
