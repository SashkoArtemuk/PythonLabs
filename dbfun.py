from models import Session, User, Wallet, Transaction
import hashlib

def create_model(model, temp):
    if temp == User:
        temp = hashlib.md5(model.psw.encode())
        model.psw = temp.hexdigest()
    session = Session()
    session.add(model)
    session.commit()

def update_user(user_id, user_data_to_update):
    session = Session()
    user_in_db = session.query(User).get(user_id)
    user_in_db.name = user_data_to_update.name
    user_in_db.login = user_data_to_update.login
    temp = hashlib.md5(user_data_to_update.psw.encode())
    user_in_db.psw = temp.hexdigest()
    session.commit()

def update_wallet(wallet_id, wallet_data_to_update):
    session = Session()
    wallet_in_db = session.query(Wallet).get(wallet_id)
    wallet_in_db.name = wallet_data_to_update.name
    wallet_in_db.ballance = wallet_data_to_update.ballance
    session.commit()

def get_model_by_login(type, login):
    session = Session()
    return session.query(type).filter_by(login=login).first()

def get_model_by_id(type, model_id):
    session = Session()
    return session.query(type).get(model_id)

def delete_model_by_id(type, model_id):
    session = Session()
    session.query(type).filter_by(id=model_id).delete()
    session.commit()

def list_transactions_for_wallet(wallet_id):
    session = Session()

    transactions = session.query(Transaction).filter(Transaction.sender_wallet_id == wallet_id).all()
    transactions.extend(session.query(Transaction).filter(Transaction.recevier_wallet_id == wallet_id).all())

    return transactions

def list_wallet_for_user(user_id):
    session = Session()
    wallets = session.query(Wallet).filter(Wallet.user_id==user_id).all()
    return wallets

def list_transactions_for_user(user_id):
    wallet_list = list_wallet_for_user(user_id)
    transactions = []
    for wallet in wallet_list:
        transactions.extend(list_transactions_for_wallet(wallet.id))
    return transactions