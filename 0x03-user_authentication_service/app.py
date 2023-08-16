#!/usr/bin/env python3
"""Starts up a flask application"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
        GET /
        Return:
            Json payload data
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    POST /users
    Register new users with email and password
    Return:
        Json payload
   """
    data = request.form

    if 'email' not in data:
        return jsonify({"message": "email required"})
    elif 'password' not in data:
        return jsonify({"message": "password required"})

    email = data.get('email')
    password = data.get('password')
    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({
            'email': email, 'message': 'user created'
            })
    except ValueError:
        return jsonify({"message": "email already registered"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
