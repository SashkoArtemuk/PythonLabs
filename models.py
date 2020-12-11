from sqlalchemy import Column, Integer, String, Boolean, orm, ForeignKey, DateTime
import os
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime

DB_URI = os.getenv("DB_URI", "postgresql://postgres:12345678@localhost/sashkodbforpp")
engine = create_engine(DB_URI)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    login= Column(String)
    psw = Column(String)

    def __init__(self, name, login, psw):
        self.name = name
        self.login = login
        self.psw =psw

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey(User.id))
    currency = Column(String)
    ballance = Column (Integer)

    user = orm.relation(User, backref="walets", lazy = "joined")

    def __init__(self, name, user_id, currency, ballance):
        self.name = name
        self.user_id = user_id
        self.currency = currency
        self.ballance = ballance

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "currency": self.currency,
            "ballance": self.ballance,
        }
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, unique=True)
    sender_wallet_id = Column(Integer, ForeignKey(Wallet.id))
    recevier_wallet_id = Column(Integer, ForeignKey(Wallet.id))
    amount = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    send_from = orm.relationship(Wallet, foreign_keys=[sender_wallet_id], backref="transactions_from", lazy="joined")
    send_to = orm.relationship(Wallet, foreign_keys=[recevier_wallet_id], backref="transactions_to", lazy="joined")

    def __init__(self, sender_wallet_id, receiver_wallet_id, amoung):
        self.sender_wallet_id = sender_wallet_id
        self.recevier_wallet_id = receiver_wallet_id
        self.amoung = amoung
