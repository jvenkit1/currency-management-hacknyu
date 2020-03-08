import os

def readFromBlockchain():
    """
    Function reads requested data from the Spectral sdk blockchain
    :return: Requested data for the user
    """
    return "tester"

def writeToBlockchain(uid, amount):
    """
    Fuction commits a new transaction block.
    :param uid: Unique user id
    :param amount: The amount to be credited to the user
    :return: Success/failure on the operation
    """
    print("Writing {} for user {}".format(amount, uid))

