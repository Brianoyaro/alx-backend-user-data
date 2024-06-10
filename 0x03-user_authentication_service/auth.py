#!/usr/bin/env python3
'''authentication module
'''
from sqlalchemy.orm.exc import NoResultFound
import uuid
import bcrypt
from db import DB
from user import User
from typing import TypeVar, Union


def _hash_password(password: str) -> bytes:
    '''hashes a password
    '''
    hashed_passwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_passwd

def _generate_uuid() -> str:
    '''generates random unique ID
    '''
    return str(uuid.uuid4())

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        '''registers a user in the database
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        '''session = self._db._session
        user = session.query(User).filter_by(email=email).first()'''
        if user is not None:
            raise ValueError('User {} already exists'.format(email))
        hashed_passwd = _hash_password(password)
        user = self._db.add_user(email, hashed_passwd)
        '''user = User(email=email, hashed_password=hashed_passwd)
        session.add(user)
        session.commit()'''
        return user

    def valid_login(self, email: str, password: str) -> bool:
        '''validates a user's password
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        '''session = self._db._session
        user = session.query(User).filter_by(email=email).first()'''
        if user is None:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        '''creates a session
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        '''session = self._db._session
        user = session.query(User).filter_by(email=email).first()'''
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        '''user.session_id = session_id
        session.add(user)
        session.commit()'''
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[TypeVar('User'), None]:
        '''retrieves a user from a given session_id
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            user = None
        '''session = self._db._session
        user = session.query(User).filter_by(session_id=session_id).first()'''
        if user is None or session_id is None:
            return None
        return user

    def destroy_session(user_id: int) -> None:
        '''deletes a user's session
        '''
        try:
            user = self._db.find_user_by(user_id=user_id)
        except NoResultFound:
            user = None
        if user is not None:
            self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(email: str) -> str:
        '''generates reset_token
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(reset_token: str, password: str) -> None:
        '''updates a user's password
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())
        self._db.update_user(user.id, hashed_password=hased_pw, reset_token=None)
        return None
