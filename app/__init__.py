from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Cargar la configuración
    from app.config import Config
    app.config.from_object(Config)

    # Inicializar la base de datos
    from .extensions.db import db
    db.init_app(app)

    # Inicializar servicio de encriptación (si lo usas)
    from app.extensions.encryption import EncryptionService
    app.encryption_service = EncryptionService(app.config['SECRET_KEY'])

    # ✅ Habilitar CORS en toda la aplicación
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # Importar y registrar Blueprints
    from app.blueprints.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blueprints.buildings.routes import buildings_bp
    app.register_blueprint(buildings_bp, url_prefix='/buildings')

    return app