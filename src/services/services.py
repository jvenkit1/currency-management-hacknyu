from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.server import Server
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
from flask import Flask, Response, jsonify
from src.dao import dao

def welcome():
    return "Hello World!!", None

def wallet(uid):
    """
    This function queries the blockchain and returns the details of the user and the wallet details
    """
    username = dao.readFromBlockchain()
    return jsonify(username=username,
                   userid=uid), None

def chargeUser(uid, amount):
    """
    Charge the user for a transaction.
    """

    def createAccount(public_key):
        response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
        if response.status_code == 200:
            print(f"SUCCESS! You have a new account")
        else:
            print(f"ERROR! Response")

    def createUser():
        pair = Keypair.random()
        print(f"Secret: {pair.secret}")
        # Secret: SCMDRX7A7OVRPAGXLUVRNIYTWBLCS54OV7UH2TF5URSG4B4JQMUADCYU
        print(f"Public Key: {pair.public_key}")
        # Public Key: GAG7SXULMNWCW6LX42JKZOZRA2JJXQT23LYY32OXA6XECUQG7RZTQJHO
        return pair

    master = createUser()
    worker = createUser()
    createAccount(master.public_key)
    createAccount(worker.public_key)

    def getAccountIfExists(public_key):
        try:
            return server.load_account(public_key)
        except NotFoundError:
            return None

    server = Server("https://horizon-testnet.stellar.org")
    master_private_key = Keypair.from_secret(master.secret)
    worker_public_key = worker.public_key
    worker_private_key = Keypair.from_secret(worker.secret)

    def sendMoney(source_public_key, source_private_key, destination_public_key, amt):
        base_fee = server.fetch_base_fee()
        transaction = (
            TransactionBuilder(
                source_account=getAccountIfExists(source_public_key),
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=base_fee,
            )
                # Because Stellar allows transaction in many currencies, you must specify the asset type.
                # Here we are sending Lumens.
                .append_payment_op(destination=destination_public_key, amount=str(amt), asset_code="XLM")
                # A memo allows you to add your own metadata to a transaction. It's
                # optional and does not affect how Stellar treats the transaction.
                .add_text_memo("Test Transaction")
                # Wait a maximum of three minutes for the transaction
                .set_timeout(10)
                .build()
        )

    # Sign the transaction to prove you are actually the person sending it.
        transaction.sign(source_private_key)
        return transaction

    transaction = sendMoney(worker.public_key, worker_private_key, master.public_key, 100)

    try:
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}{response}")

def rewardUser(uid, amount):
    """
    Reward the user by increasing his karma points via blockchain
    """
    def createAccount(public_key):
        response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
        if response.status_code == 200:
            print(f"SUCCESS! You have a new account")
        else:
            print(f"ERROR! Response")

    def createUser():
        pair = Keypair.random()
        print(f"Secret: {pair.secret}")
        # Secret: SCMDRX7A7OVRPAGXLUVRNIYTWBLCS54OV7UH2TF5URSG4B4JQMUADCYU
        print(f"Public Key: {pair.public_key}")
        # Public Key: GAG7SXULMNWCW6LX42JKZOZRA2JJXQT23LYY32OXA6XECUQG7RZTQJHO
        return pair

    master = createUser()
    worker = createUser()
    createAccount(master.public_key)
    createAccount(worker.public_key)

    def getAccountIfExists(public_key):
        try:
            return server.load_account(public_key)
        except NotFoundError:
            return None

    server = Server("https://horizon-testnet.stellar.org")
    master_private_key = Keypair.from_secret(master.secret)
    worker_public_key = worker.public_key
    worker_private_key = Keypair.from_secret(worker.secret)

    def sendMoney(source_public_key, source_private_key, destination_public_key, amt):
        base_fee = server.fetch_base_fee()
        transaction = (
            TransactionBuilder(
                source_account=getAccountIfExists(source_public_key),
                network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                base_fee=base_fee,
            )
                # Because Stellar allows transaction in many currencies, you must specify the asset type.
                # Here we are sending Lumens.
                .append_payment_op(destination=destination_public_key, amount=str(amt), asset_code="XLM")
                # A memo allows you to add your own metadata to a transaction. It's
                # optional and does not affect how Stellar treats the transaction.
                .add_text_memo("Test Transaction")
                # Wait a maximum of three minutes for the transaction
                .set_timeout(10)
                .build()
        )

    # Sign the transaction to prove you are actually the person sending it.
        transaction.sign(source_private_key)
        return transaction


    transaction = sendMoney(master.public_key, master_private_key, worker.public_key, 100)

    try:
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}{response}")


    transaction = sendMoney(worker.public_key, worker_private_key, master.public_key, 100)

    try:
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}{response}")
