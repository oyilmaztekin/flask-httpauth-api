# -*- coding: UTF-8 -*-
# coding:utf-8

from flask import Flask, abort, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
import humanize


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

from models import *

@app.route('/api/user', methods=['POST'])
def createUser():
    email = request.json.get('email')
    sifre = request.json.get('sifre')
    tarih = datetime.now()
    
    if email is None or sifre is None or tarih is None:
    	abort(400)

    user = User(email=email, sifre=sifre, tarih=tarih)
    # -- kullanıcı mevcut mu? -- #
   
    if User.query.filter_by(email = email).first() is not None:
    	return jsonify({'email': "bu mail adresi kullanılıyor"}), 201, {'location':url_for('createUser', id = user.id, _external = True, )}

    user.hash_password(sifre)
    db.session.add(user)
    db.session.commit()

    return jsonify({'email':user.email}), 201, {'location':url_for('createUser', id = user.id, _external = True)}


if __name__ == '__main__':
    app.run()


