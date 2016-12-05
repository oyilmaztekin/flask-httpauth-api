# -*- coding: UTF-8 -*-
# coding:utf-8

from flask import Flask, abort, request, url_for, jsonify, session
import json
from flask_sqlalchemy import SQLAlchemy
from models import *
import requests
from datetime import datetime
import sys
import re
import jwt
from flask_httpauth import HTTPBasicAuth

Email_Regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

auth = HTTPBasicAuth()

app.config["SECRET_KEY"] = '6cf34ed05e241ac72456425779220bfeaf3557ef8371bed4'
#app.config["DEBUG"] = True
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SESSION_COOKIE_SECURE'] = True

@app.route('/api/user', methods=['POST'])
def createUser():
    email = request.json.get('email')
    sifre = request.json.get('sifre')
    tarih = datetime.now()
    is_active = request.json.get('is_active') 
    
    if email is None or sifre is None:
    	abort(400)
		
    user = User(email=email, sifre=sifre, tarih=tarih, is_active=is_active)
    user.hash_password(sifre)
    token = jwt.encode({'JWT': user.sifre+str(tarih)+email+str(is_active)}, 'secret', algorithm='HS256')
    # -- kullanıcı mevcut mu? -- #
   
    if User.query.filter_by(email = email).first() is not None:
    	return jsonify({'hata': "bu mail adresi kullanımda"}), 201, {'location':url_for('createUser', id = user.id, _external = True, )}
	
    if not Email_Regex.match(email):
    	return jsonify({"hata":"Mail adresi düzgün yazılmadı."})
	
    db.session.add(user)
    db.session.commit()
    return jsonify({'mesaj': "Hesabınız oluşturuldu", 'token':'JWT ' + token}),  201, {'location':url_for('createUser', id = user.id)}

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
	
	result = []
	for item in user.alarm:
	    result.append({
	        "id": item.id,
	        "dovizAdi": item.dovizAdi,
	        "mevcutDeger": item.mevcutDeger,
	        "beklenenDeger": item.beklenenDeger,
	        "oranTuru": item.oranTuru,
	        "tarih": item.tarih
	    })
	return jsonify(result, {'ses':session['_id']})


@app.route('/api/alarm-olustur', methods=['POST'])
@auth.login_required
def alarm_olustur():
	
	dovizAdi = request.json.get('dovizAdi')
	mevcutDeger = request.json.get('mevcutDeger')
	beklenenDeger = request.json.get('beklenenDeger')
	oranTuru = request.json.get('oranTuru')
	tarih = datetime.now()
	deviceID = request.json.get('deviceID')
	user_id = current_user.id
	isIOS = request.json.get('isIOS')
	isAndroid = request.json.get('isAndroid')

	if dovizAdi is None or beklenenDeger is None or oranTuru is None or user_id is None:
		abort(400)

	alarm = Alarm(dovizAdi=dovizAdi, mevcutDeger=mevcutDeger, beklenenDeger=beklenenDeger, oranTuru=oranTuru, tarih=tarih, deviceID=deviceID, user_id=user_id, isIOS=isIOS, isAndroid=isAndroid)

	db.session.add(alarm)
	db.session.commit()

	return jsonify({
		"mesaj": "Alarm başarı ile oluşturuldu"
		},
		{
	        "id": alarm.id,
	        "dovizAdi": alarm.dovizAdi,
	        "mevcutDeger": alarm.mevcutDeger,
	        "beklenenDeger": alarm.beklenenDeger,
	        "oranTuru": alarm.oranTuru,
	        "tarih": alarm.tarih
	    })


@app.route('/api/alarm', methods=['GET'])
@auth.login_required
def alarm():
	user = current_user
	result = []
	for item in user.alarm:
	    result.append({
	        "id": item.id,
	        "dovizAdi": item.dovizAdi,
	        "mevcutDeger": item.mevcutDeger,
	        "beklenenDeger": item.beklenenDeger,
	        "oranTuru": item.oranTuru,
	        "tarih": item.tarih
	    })
	return jsonify(result)


#API HANDLE 

#header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Basic NDkwY2UxYTYtN2QzNC00ZWM5LTg3YzAtMWE3YWZhNzM3NDlj"}

#payload = {"app_id": "2c4ad89e-0d71-41a1-960c-682fc7411e98", "included_segments": ["All"], "contents": {"en": "English Message"}}
 
#req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))
 
#print(req.status_code, req.reason)

if __name__ == '__main__':
    app.run()

			
			