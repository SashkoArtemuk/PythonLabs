from flask import Flask, jsonify, request, Response
from gevent.pywsgi import WSGIServer
import json
import schemas
import dbfun
from models import User, Wallet, Transaction
from error import Error
from flask_httpauth import HTTPBasicAuth
import hashlib

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(login, password):
        user = dbfun.get_model_by_login(User, login)
        if user and user.psw == hashlib.md5(password.encode()).hexdigest():
            return user.id



@app.route('/users', methods=['POST'])
def create_user():
    try:
        user_to_get = schemas.CreatingUser().load(request.json)
        user = User(**user_to_get)
        dbfun.create_model(user, User)
        return jsonify(schemas.ValidateError().dump(Error(200, "OK", "Ok")))
    except:
        return Response(
            response=json.dumps({"message": "Invalid input"}),
            status=400,
            mimetype="application/json"
        )

@app.route('/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user_by_id(user_id):
    if user_id != auth.current_user():
        return Response(
                response=json.dumps({"message": "Forbidden"}),
                status=403,
                mimetype="application/json"
            )
    user = dbfun.get_model_by_id(User, user_id)
    return jsonify(schemas.UserToSend().dump(user))


@app.route('/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user_by_id(user_id):
    if user_id != auth.current_user():
        return Response(
                response=json.dumps({"message": "Forbidden"}),
                status=403,
                mimetype="application/json"
            )
    try:
        user_to_get = schemas.CreatingUser().load(request.json)
        new_user = User(**user_to_get)
        dbfun.update_user(user_id, new_user)
        return jsonify(schemas.ValidateError().dump(Error(200, "OK", "Ok")))
    except:
        return Response(
            response=json.dumps({"message": "Invalid input"}),
            status=400,
            mimetype="application/json"
        )

@app.route('/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user_by_id(user_id):
    if user_id != auth.current_user():
        return Response(
                response=json.dumps({"message": "Forbidden"}),
                status=403,
                mimetype="application/json"
            )
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
        return Response(
            response=json.dumps({"message": "Invalid input"}),
            status=400,
            mimetype="application/json"
        )

@app.route('/wallet/<int:wallet_id>', methods=['PUT'])
@auth.login_required
def update_wallet(wallet_id):
    try:
        if dbfun.get_model_by_id(Wallet, wallet_id).user_id != auth.current_user():
            return Response(
                response=json.dumps({"message": "Forbidden"}),
                status=403,
                mimetype="application/json"
            )
        wallet_to_get = schemas.WalletToGet().load(request.json)
        wallet = Wallet(**wallet_to_get)
        dbfun.update_wallet(wallet_id, wallet)
        reply = Error(200, "OK", "OK")
        return jsonify(schemas.ValidateError().dump(reply))
    except:
        return Response(
            response=json.dumps({"message": "Invalid input"}),
            status=400,
            mimetype="application/json"
        )

@app.route('/wallet/<int:wallet_id>', methods=['GET'])
@auth.login_required
def get_wallet_by_id(wallet_id):
    if dbfun.get_model_by_id(Wallet, wallet_id).user_id != auth.current_user():
        return Response(
            response=json.dumps({"message": "Forbidden"}),
            status=403,
            mimetype="application/json"
        )
    wallet_to_send = dbfun.get_model_by_id(Wallet, wallet_id)
    return jsonify(schemas.WalletToSend().dump(wallet_to_send))

@app.route('/wallet/<int:wallet_id>', methods=['DELETE'])
@auth.login_required
def delete_wallet_by_id(wallet_id):
    if dbfun.get_model_by_id(Wallet, wallet_id).user_id != auth.current_user():
        return Response(
            response=json.dumps({"message": "Forbidden"}),
            status=403,
            mimetype="application/json"
        )
    dbfun.delete_model_by_id(Wallet, wallet_id )
    return jsonify(schemas.ValidateError().dump(Error(200, "OK", "OK")))

@app.route('/wallet/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_wallets_by_user_id(user_id):
    if user_id != auth.current_user():
        return Response(
            response=json.dumps({"message": "Forbidden"}),
            status=403,
            mimetype="application/json"
        )
    wallet_list = dbfun.list_wallet_for_user(user_id)
    return jsonify(schemas.WalletToSend().dump(wallet_list, many = True))

@app.route('/transaction', methods=['POST'])
@auth.login_required
def create_transaction():
    try:
        transaction_data = schemas.ValidateTransaction().load(request.json)
        transaction = Transaction(**transaction_data)
        if dbfun.get_model_by_id(Wallet, transaction.sender_wallet_id).user_id != auth.current_user():
            return Response(
                response=json.dumps({"message": "Forbidden"}),
                status=403,
                mimetype="application/json"
            )

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
        return Response(
            response=json.dumps({"message": "Invalid input"}),
            status=400,
            mimetype="application/json"
        )

@app.route('/transaction/<int:transaction_id>', methods=['GET'])
@auth.login_required
def get_transaction_by_id(transaction_id):
    transaction = dbfun.get_model_by_id(Transaction, transaction_id)
    if transaction and transaction.sender_wallet_id != auth.current_user() and transaction.recevier_wallet_id != auth.current_user():
        return Response(
            response=json.dumps({"message": "Forbidden"}),
            status=403,
            mimetype="application/json"
        )
    return jsonify(schemas.ValidateTransaction().dump(transaction))

@app.route('/transaction/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_transactions_by_user_id(user_id):
    if user_id != auth.current_user():
        return Response(
                response=json.dumps({"message": "Forbidden"}),
                status=403,
                mimetype="application/json"
            )
    transaction = dbfun.list_transactions_for_user(user_id)
    return jsonify(schemas.ValidateTransaction().dump(transaction, many=True))

@app.route('/wallet/<int:wallet_id>/transaction', methods=['GET'])
@auth.login_required
def get_transactions_by_wallet_id(wallet_id):
    if dbfun.get_model_by_id(Wallet, wallet_id).user_id != auth.current_user():
        return Response(
            response=json.dumps({"message": "Forbidden"}),
            status=403,
            mimetype="application/json"
        )
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
