from flask import Flask, request
from src.services import services

def create():
    app=Flask(__name__)

    @app.route('/rewardUser', methods=['POST'])
    def reward():
        print("Inside reward user")

        json_data = request.json

        error = services.rewardUser(json_data['uid'], json_data['amount'])
        if(error):
            print("Error observed")
            return 400
        return '', 201

    @app.route('/chargeUser', methods=['POST'])
    def charge():
        print("Inside charge user")

        json_data = request.json

        error = services.chargeUser(json_data['uid'], json_data['amount'])
        if(error):
            print("Error observed")

    @app.route('/wallet', methods=['GET'])
    def wallet():
        print("Inside wallet info for user")

        json_data = request.json

        data, error = services.wallet(json_data['uid'])
        if(error):
            print("Error observed")
        return data

    @app.route('/', methods=['GET'])
    def index():
        return 'Hello World'

    return app
