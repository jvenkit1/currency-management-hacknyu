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
    return None

def rewardUser(uid, amount):
    """
    Reward the user by increasing his karma points via blockchain
    """
    return None
