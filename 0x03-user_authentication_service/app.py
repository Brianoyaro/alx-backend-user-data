#!/usr/bin/env python3
'''application entry point module
'''
from flask import Flask, jsonify, request, abort, make_response, redirect, url_for
from auth import Auth
from user import User


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def index():
    '''index point of application
    '''
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def post_users():
    '''registers a user
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": email, "message": "user created"})

@app.route('/sessions', methods=['POST'])
def login():
    '''logs in a user
    '''
    email = request.form.get('email')
    password = request.form.get('password')
    is_valid_login = AUTH.valid_login(email, password)
    if not is_valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    user = AUTH._db.find_user_by(email=email)
    AUTH._db.update_user(user.id, session_id=session_id)
    '''user.session_id = session_id
    AUTH._db._session.add(user)
    AUTH._db._session.commit()'''
    # DEBUGGING
    '''uz = AUTH._db._session.query(User).all()
    for u in uz:
        print(u.id, u.email, u.hashed_password, u.session_id)'''
    response = make_response({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response

@app.route('/sessions', methods=['DELETE'])
def logout():
    '''logs a user out
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    abort(403)

@app.route('/profile')
def profile_page():
    '''returns user's profile
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''retrieves reset token from user
    '''
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "reset_token": token})

@app.route('/reset_password', methods=['PUT'])
def reset_password():
    '''resets a user's password
    '''
    email = request.form.get('email')
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_Password")
    '''saved_request_token = AUTH.get_reset_password_token(email)
    if saved_reset_token != reset_token:
        abort(403)
    AUTH.update_password(reset_token, new_password)'''
    try:
        # user = AUTH._db.find_user_by(reset_token=reset_token, email=email)
        user = AUTH._db.find_user_by(email=email)
    except NoResultFound:
        abort(403)
    else:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    # return jsonify({"email": email, "message": "Password updated"})



if __name__ == "__main__":
    # app.run(host="0.0.0.0", port="5000")
    app.run(host="0.0.0.0", port="5000", debug=True)
