#!/usr/bin/env python3
""" Module of Session views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_handler() -> str:
    """
    handles all routes for the Session authentication
    """
    email = request.form.get('email')
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) <= 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 404
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    out = jsonify(user.to_json())
    out.set_cookie(getenv('SESSION_NAME'), session_id)
    return out


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout_handler() -> str:
    """
    logout the current user session
    """
    from api.v1.app import auth
    ret = auth.destroy_session(request)
    if ret is False:
        abort(404)
    return jsonify({}), 200
