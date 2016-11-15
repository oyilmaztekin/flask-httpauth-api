# -*- coding: UTF-8 -*-
# coding:utf-8

from flask import Flask, abort, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import humanize
from flask_login import LoginManager, login_user, current_user



app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

from models import *

app.config["SECRET_KEY"] = '6cf34ed05e241ac72456425779220bfeaf3557ef8371bed4'
#app.config["DEBUG"] = True
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SESSION_COOKIE_SECURE'] = True

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)

@app.route('/api/user', methods=['POST'])
def createUser():
    email = request.json.get('email')
    sifre = request.json.get('sifre')
    tarih = datetime.now()
    is_active = request.json.get('is_active')
    
    if email is None or sifre is None:
    	abort(400)

    user = User(email=email, sifre=sifre, tarih=tarih, is_active=is_active)
    # -- kullanıcı mevcut mu? -- #
   
    if User.query.filter_by(email = email).first() is not None:
    	return jsonify({'hata': "bu mail adresi kullanımda"}), 201, {'location':url_for('createUser', id = user.id, _external = True, )}

    user.hash_password(sifre)
    db.session.add(user)
    db.session.commit()
    login_user(user)

    return jsonify({'email':user.email}), 201, {'location':url_for('createUser', id = user.id, _external = True)}


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()
    try:
    	pass
    except DoesNotExist:
    	logging.warning("Kullanıcı mevcut değil")


@app.route('/api/login', methods=['POST'])
def login():
	if current_user.is_authenticated:
		return jsonify({'mesaj':'Zaten giriş yaptınız'}), 201, {'location':url_for('login', id= user.id, _external = True)}
	
	email = request.json.get('email')
	sifre = request.json.get('sifre')

	user = User.query.filter_by(email=email).first()
	
	if email is None or sifre is None:
		return jsonify({'hata':'kullanıcı adı veya şifre hatası'}), 201, {'location':url_for('login', id= user.id, _external = True)}

	user.verify_password(sifre)
	login_user(user)

	return jsonify({'email':user.email}), 201, {'location':url_for('login', id= user.id, _external = True)}



if __name__ == '__main__':
    app.run()


