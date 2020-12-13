from flask import Flask, jsonify, request, Response
from gevent.pywsgi import WSGIServer
import json
import schemas
import dbfun
from models import User, Wallet, Transaction
from error import Error
app = Flask(__name__)

@app.route('/api/v1/hello-world-1')
def hello_world():
    return 'Hello World - 1'

@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_to_get = schemas.CreatingUser().load(request.json)
        user = User(**user_to_get)
        dbfun.create_model(user, User)
        return jsonify(schemas.ValidateError().dump(Error(200, "OK", "Ok")))
    except:
        return jsonify(schemas.ValidateError().dump(Error(400, "INVALID_INPUT", "Invalid input")))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = dbfun.get_model_by_id(User, user_id)
    return jsonify(schemas.UserToSend().dump(user))

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    try:
        user_to_get = schemas.CreatingUser().load(request.json)
        new_user = User(**user_to_get)
        dbfun.update_user(user_id, new_user)
        return jsonify(schemas.ValidateError().dump(Error(200, "OK", "Ok")))
    except:
        return jsonify(schemas.ValidateError().dump(Error(400, "INVALID_INPUT", "Invalid input")))

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    dbfun.delete_model_by_id(User, user_id)
    return jsonify(schemas.ValidateError().dump(Error(200, "OK", "Successful operation")))

@app.route('/wallet', methods=['POST'])
def create_wallet():
    try:
        wallet_to_get = schemas.WalletToGet().load(request.json)
        wallet = Wallet(**wallet_to_get)
        dbfun.create_model(wallet, Wallet)
        reply = Error(200, "OK", "OK")
        return jsonify(schemas.ValidateError().dump(reply))
    except:
        return jsonify(schemas.ValidateError().dump(Error(400, "INVALID_INPUT", "Invalid input")))

@app.route('/wallet', methods=['PUT'])
def update_wallet():
    try:
        wallet_to_get = schemas.WalletToGet().load(request.json)
        wallet = Wallet(**wallet_to_get)
        dbfun.update_wallet(wallet)
        reply = Error(200, "OK", "OK")
        return jsonify(schemas.ValidateError().dump(reply))
    except:
        return jsonify(schemas.ValidateError().dump(Error(400, "INVALID_INPUT", "Invalid input")))

@app.route('/wallet/<int:wallet_id>', methods=['GET'])
def get_wallet_by_id(wallet_id):
    wallet_to_send = dbfun.get_model_by_id(Wallet, wallet_id)
    return jsonify(schemas.WalletToSend().dump(wallet_to_send))

@app.route('/wallet/<int:wallet_id>', methods=['DELETE'])
def delete_wallet_by_id(wallet_id):
    dbfun.delete_model_by_id(Wallet, wallet_id )
    return jsonify(schemas.ValidateError().dump(Error(200, "OK", "OK")))

@app.route('/wallet/users/<int:user_id>', methods=['GET'])
def get_wallets_by_user_id(user_id):
    wallet_list = dbfun.list_wallet_for_user(user_id)
    return jsonify(schemas.WalletToSend().dump(wallet_list, many = True))

@app.route('/transaction', methods=['POST'])
def create_transaction():
    try:
        transaction_data = schemas.ValidateTransaction().load(request.json)
        transaction = Transaction(**transaction_data)

        if dbfun.get_model_by_id(Wallet, transaction.sender_wallet_id).ballance < transaction.amount:
            transaction.amount = 0
        if dbfun.get_model_by_id(Wallet, transaction.sender_wallet_id).currency != dbfun.get_model_by_id(Wallet, transaction.recevier_wallet_id).currency:
            transaction.amount = 0

        recevier_wallet = dbfun.get_model_by_id(Wallet, transaction.recevier_wallet_id)
        recevier_wallet.ballance += transaction.amount

        sender_wallet = dbfun.get_model_by_id(Wallet, transaction.sender_wallet_id)
        sender_wallet.ballance -= transaction.amount

        dbfun.update_wallet(transaction.sender_wallet_id, sender_wallet)
        dbfun.update_wallet(transaction.recevier_wallet_id, recevier_wallet)

        dbfun.create_model(transaction, Transaction)
        return jsonify(schemas.ValidateError().dump(Error(200, "OK", "OK")))
    except:
        return jsonify(schemas.ValidateError().dump(Error(400, "INVALID_INPUT", "Invalid input")))

@app.route('/transaction/<int:transaction_id>', methods=['GET'])
def get_transaction_by_id(transaction_id):
    transaction = dbfun.get_model_by_id(Transaction, transaction_id)
    return jsonify(schemas.ValidateTransaction().dump(transaction))

@app.route('/transaction/users/<int:user_id>', methods=['GET'])
def get_transactions_by_user_id(user_id):
    transaction = dbfun.list_transactions_for_user(user_id)
    return jsonify(schemas.ValidateTransaction().dump(transaction, many=True))

@app.route('/wallet/<int:wallet_id>/transaction', methods=['GET'])
def get_transactions_by_wallet_id(wallet_id):
    transaction_list = dbfun.list_transactions_for_wallet(wallet_id)
    return jsonify(schemas.ValidateTransaction().dump(transaction_list, many=True))

@app.errorhandler(404)
def page_not_found(e):
    reply = Error(404, "NOT_FOUND", "Page not found")
    return  jsonify(schemas.ValidateError().dump(reply))

@app.errorhandler(400)
def page_not_found(e):
    reply = Error(400, "BAD_REQUEST", "Bad request")
    return  jsonify(schemas.ValidateError().dump(reply))

@app.errorhandler(405)
def method_not_allowed(e):
    reply = Error(404, "METHOD_NOT_ALLOWED", "Method not allowed")
    return jsonify(schemas.ValidateError().dump(reply))

if __name__ == '__main__':
    app.run(debug=True)

#http_server = WSGIServer(('', 5000), app)
#http_server.serve_forever()
