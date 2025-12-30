from flask import Flask
from app.routes.routes import main_bp
from app.extension import db, migrate
from app.models.models import Product,Customer

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.register_blueprint(main_bp)
    db.init_app(app)
    migrate.init_app(app,db)
    return app