#!/usr/bin/env python3
"""Starts up a flask application"""
from flask import Flask, jsonify, request, make_response, abort
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
def login() -> str:
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
def logout() -> None:
    """Log out from a login session"""
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('index'))
        else:
            abort(403)
    else:
        abort(403)


@app.route('/profile', methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ GET /profile
        get user info using the session id
        Return:
            Json Payload
    """
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})
        else:
            abort(403)
    else:
        abort(403)


@app.route('/reset_password', methods=["POST"], strict_slashes=False)
def reset_token() -> str:
    """Generate a reset_token"""
    data = request.form
    if 'email' in data:
        email = data.get('email')
        try:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": reset_token})
        except ValueError:
            abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def reset_password() -> str:
    """Reset user password"""
    data = request.form
    if 'email' not in data:
        return jsonify({"message": "email required"}), 400
    if 'password' not in data:
        return jsonify({"message": "password required"}), 400
    if 'reset_token' not in data:
        return jsonify({"message": "reset_token required"}), 400
    else:
        email = data.get('email')
        password = data.get('password')
        reset_token = data.get('reset_token')
        try:
            AUTH.update_password(reset_token, password)
            return jsonify({"email": email, "message": "Password updated"})
        except ValueError:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
