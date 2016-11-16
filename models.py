# -*- coding: UTF-8 -*-
# coding:utf-8
from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    sifre = db.Column(db.String(40), nullable=False)
    tarih = db.Column(db.DateTime())
    is_active = db.Column(db.Boolean())
    alarm = db.relationship('Alarm', backref='user', lazy='dynamic')

    def __init__(self, email, tarih, sifre, is_active):
        self.email = email
        self.tarih = tarih
        #if tarih is None:
            #self.tarih = datetime.now()
        if is_active is None:
            self.is_active = True
        self.tarih = tarih
        self.sifre = sifre

    def hash_password(self, password):
        self.sifre = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.sifre)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(str(self.id))

    def __repr__(self):
        return '<User %r>' % self.email

class Alarm(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    dovizAdi = db.Column(db.String(30))
    mevcutDeger = db.Column(db.String(30))
    beklenenDeger = db.Column(db.String(30))
    oranTuru = db.Column(db.String(10))
    tarih = db.Column(db.DateTime())
    deviceID = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, dovizAdi, tarih, user_id, mevcutDeger, beklenenDeger, oranTuru, deviceID):
        self.dovizAdi = dovizAdi
        self.mevcutDeger = mevcutDeger
        self.beklenenDeger = beklenenDeger
        self.oranTuru = oranTuru
        self.deviceID = deviceID
        self.user_id = user_id
        
        if tarih is None:
            tarih = datetime.now()
        self.tarih = tarih

    def __repr__(self):
        return '<Alarm %r>' % self.dovizAdi
