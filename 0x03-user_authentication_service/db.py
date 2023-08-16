#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database"""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs: dict) -> User:
        """Return first row found in users table based on keywords"""
        if not kwargs:
            raise InvalidRequestError
        defult_columns = [
            'id',
            'email',
            'hashed_password',
            'session_id',
            'reset_token'
            ]
        for arg in kwargs:
            if arg not in defult_columns:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs: dict) -> None:
        """Update a user object from the database"""

        user = DB.find_user_by(self, id=user_id)
        defult_columns = [
            'id',
            'email',
            'hashed_password',
            'session_id',
            'reset_token'
            ]
        for key, value in kwargs.items():
            if key in defult_columns:
                setattr(user, key, value)
            else:
                raise ValueError

        self._session.commit()