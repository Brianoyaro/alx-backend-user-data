#!/usr/bin/env python3
'''main test base
'''
import requests


def register_user(email: str, password: str) -> None:
    '''asserts register user
    '''
    url = 'localhost:5000/users'
    method = 'post'
    data = {'email': email, 'password': password}
    value = requests.post(url, data=data)
    assert value.json() == {"email": email, "message": "user created"}
    assert 200 == value.status_code


def log_in_wrong_password(email: str, password: str) -> None:
    '''asserts wrong log in
    '''
    url = 'localhost:5000/sessions'
    method = 'post'
    data = {'email': email, 'password': password}
    value = requests.post(url, data=data)
    assert 401 == value.status_code


def log_in(email: str, password: str) -> str:
    '''asserts login
    '''
    url = 'localhost:5000/sessions'
    method = 'post'
    data = {'email': email, 'password': password}
    value = requests.post(url, data=data)
    assert value.json() == {"email": email, "message": "logged in"}
    assert 200 == value.status_code


def profile_unlogged() -> None:
    '''asserts false profile checking
    '''
    url = 'localhost:5000/profile'
    method = 'get'
    cookies = dict()
    value = requests.get(url, cookies=cookies)
    assert 403 == value.status_code


def profile_logged(session_id: str) -> None:
    '''asserts profile checking
    '''
    url = 'localhost:5000/profile'
    method = 'get'
    cookies = {'session_id': session_id}
    value = requests.get(url, cookies=cookies)
    assert 200 == value.status_code
    assert value.json() == {"email": email}


def log_out(session_id: str) -> None:
    '''asserts logout
    '''
    url = 'localhost:5000/sessions'
    method = 'delete'
    data = {'session_id': session_id}
    value = requests.delete(url, data=data)
    assert 200 == value.status_code
    assert value.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    '''asserts reset_password_token
    '''
    url = 'localhost:5000/reset_password'
    method = 'post'
    data = {'email': email}
    value = requests.post(url, data=data)
    assert 200 == value.status_code
    assert value.json() == {"email": email,
                            "reset_token": value.json().get('reset_token')}


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''asserts uodate_password
    '''
    url = 'localhost:5000/reset_password'
    method = 'put'
    data = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password}
    value = requests.put(url, data=data)
    assert 200 == value.status_code
    assert value.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
