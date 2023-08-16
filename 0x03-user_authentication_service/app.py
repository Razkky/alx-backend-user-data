#!/usr/bin/env python3
"""Starts up a flask application"""
from flask import Flask, jsonify, request, make_response, abort,
from flask import redirect, url_for
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


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """Create new session and return session_id in header as cookie"""
    data = request.form
    if 'email' not in data:
        abort(401)
    if 'password' not in data:
        abort(401)
    try:
        email = data.get('email')
        password = data.get('password')
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = make_response(jsonify(
                    {"email": email, "message": "logged in"}
                ))
            response.set_cookie('session_id', session_id)
            return response
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout():
    """Log out from a login session"""
    data = request.form
    if 'session_id' in data:
        session_id = data.get('session_id')
        try:
            user = AUTH.get_user_from_session_id(session_id)
            AUTH.destroy_session(user.id)
            return redirect(url_for('index'))
        except Exception:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
