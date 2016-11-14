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
    alarm = db.relationship('Alarm', backref='user', lazy='dynamic')

    def __init__(self, email, tarih, sifre):
        self.email = email
        if tarih is None:
            tarih = datetime.now()
        self.tarih = tarih
        self.sifre = sifre

    def hash_password(self, password):
        self.sifre = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.sifre)

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

    def __init__(self, dovizAdi, tarih):
        self.dovizAdi = dovizAdi
        if tarih is None:
            tarih = datetime.now()
        self.tarih = tarih

    def __repr__(self):
        return '<Alarm %r>' % self.dovizAdi
