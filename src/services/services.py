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
    def load_last_paging_token():
    # Get the last paging token from a local database or file
        return "now"

    def save_paging_token(paging_token):
        # In most cases, you should save this to a local database or file so that
        # you can load it next time you stream new payments.
        pass

    server = Server("https://horizon-testnet.stellar.org")
    account_id = "GA4QPSGBHK7RAJZBBEDCIKFPSYLG3O2UTBT2I56RN4B5KIQF2GFZKSMF"

    # Create an API call to query payments involving the account.
    payments = server.payments().for_account(account_id)

    # If some payments have already been handled, start the results from the
    # last seen payment. (See below in `handle_payment` where it gets saved.)
    last_token = load_last_paging_token()
    if last_token:
        payments.cursor(last_token)

    # `stream` will send each recorded payment, one by one, then keep the
    # connection open and continue to send you new payments as they occur.
    for payment in payments.stream():
        # Record the paging token so we can start from here next time.
        save_paging_token(payment["paging_token"])

        # We only process `payment`, ignore `create_account` and `account_merge`.
        if payment["type"] != "payment":
            continue

        # The payments stream includes both sent and received payments. We
        # only want to process received payments here.
        if payment['to'] != account_id:
            continue

        # In Stellar’s API, Lumens are referred to as the “native” type. Other
        # asset types have more detailed information.
        if payment["asset_type"] == "native":
            asset = "Lumens"
        else:
            asset = f"{payment['asset_code']}:{payment['asset_issuer']}"
        print(f"{payment['amount']} {asset} from {payment['from']}")

        return None

def rewardUser(uid, amount):
    """
    Reward the user by increasing his karma points via blockchain
    """
    server = Server("https://horizon-testnet.stellar.org")
    source_key = Keypair.from_secret("SA6HHDJ5KZKYFZVOOGHENIPVKV2HGKICN4RYQ2UZNZHZP7ZIYSQIQDCI")
    destination_id = "GA4QPSGBHK7RAJZBBEDCIKFPSYLG3O2UTBT2I56RN4B5KIQF2GFZKSMF"

    # First, check to make sure that the destination account exists.
    # You could skip this, but if the account does not exist, you will be charged
    # the transaction fee when the transaction fails.
    try:
        server.load_account(destination_id)
    except NotFoundError:
        # If the account is not found, surface an error message for logging.
        raise Exception("The destination account does not exist!")

    # If there was no error, load up-to-date information on your account.
    source_account = server.load_account(source_key.public_key)

    # Let's fetch base_fee from network
    base_fee = server.fetch_base_fee()

    # Start building the transaction.
    transaction = (
        TransactionBuilder(
            source_account=source_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
            # Because Stellar allows transaction in many currencies, you must specify the asset type.
            # Here we are sending Lumens.
            .append_payment_op(destination=destination_id, amount="10", asset_code="XLM")
            # A memo allows you to add your own metadata to a transaction. It's
            # optional and does not affect how Stellar treats the transaction.
            .add_text_memo("Test Transaction")
            # Wait a maximum of three minutes for the transaction
            .set_timeout(10)
            .build()
    )

    # Sign the transaction to prove you are actually the person sending it.
    transaction.sign(source_key)

    try:
        # And finally, send it off to Stellar!
        response = server.submit_transaction(transaction)
        print(f"Response: {response}")
    except (BadRequestError, BadResponseError) as err:
        print(f"Something went wrong!\n{err}")

    return None
