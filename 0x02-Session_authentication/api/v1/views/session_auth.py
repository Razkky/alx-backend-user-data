#!/usr/bin/env python3
"""Contais route to sesssion Auth"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def session_auth_login() -> str:
    """
        POST /auth_session/login
        Return User in json format
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            from api.v1.auth.session_auth import SessionAuth
            session_name = os.getenv("SESSION_NAME")
            auth = SessionAuth()
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(session_name, session_id)
            return response
        else:
            return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=["DELETE"],
                 strict_slashes=False)
def session_logout() -> str:
    """
        DELETE /api/v1/auth_session/logut
        logout a user from a sessiona and
        return empty json
    """
    from api.v1.app import auth
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
    try:
        auth.destroy_session(request)
    except Exception:
        abort(404)
    return jsonify({}), 200
