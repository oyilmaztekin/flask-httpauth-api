# -*- coding: UTF-8 -*-
# coding:utf-8

from flask import Flask, abort, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

from models import *

@app.route('/api/user', methods=['POST'])
def createUser():
    email = request.json.get('email')
    sifre = request.json.get('sifre')
    tarih = request.json.get('tarih')

    if email is None or sifre is None:
    	abort(400)

    # -- kullanıcı mevcut mu? -- #
    #if User.query.filter_by(email = email).first() is not None:
    	#abort(400)

    user = User(email=email, tarih=tarih)
    user.hash_password(sifre)
    db.session.add(user)
    db.session.commit()

    return jsonify({'email':user.email}), 201, {'location':url_for('createUser',id = user.id, _external = True)}


if __name__ == '__main__':
    app.run()



