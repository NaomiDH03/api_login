import os
from datetime import timedelta, datetime
from email_validator import validate_email, EmailNotValidError
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import db, User
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Expiraciones
access_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRES', 15))
reset_days = int(os.getenv('REFSET_TOKEN_EXPIRES', 7))



def _require_json(keys):
    data = request.get_json()
    missing = [key for key in keys if key not in data or data[key] in [None, '']]
    if missing:
        return jsonify({'error': f'Campos faltantes: {", ".join(missing)}'}), 400
    return data, None