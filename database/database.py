import os
from datetime import datetime, UTC

import redis
import sqlalchemy as alc
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from argon2 import PasswordHasher
from dotenv import load_dotenv, find_dotenv

import logs as log


load_dotenv(find_dotenv())


REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWD = os.getenv('MYSQL_PASSWD', 'passwd')
MYSQL_DB = os.getenv('MYSQL_DB', 'fastapi-app-template')


# Password hasher
# ph = PasswordHasher()


class RedisClient:
    """Redis client wrapper class"""
    
    @classmethod
    def check_access(cls) -> bool:
        """
        Checks connection to Redis database
        
        Returns:
            bool: True if connection established, False otherwise
        """
        try:
            redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0).ping()
            return True
        
        except redis.ConnectionError:
            return False
    
    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        
    def __enter__(self):
        """
        Enter context manager and return Redis client.
        
        Returns:
            redis.Redis: Redis client instance for use in with statement
        """
        return self.client
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager and handle exceptions.
        
        Args:
            exc_type: Exception type if exception occurred, None otherwise
            exc_val: Exception value if exception occurred, None otherwise  
            exc_tb: Exception traceback if exception occurred, None otherwise
            
        Returns:
            bool: True to suppress exception if handled, else raises exception
            
        Raises:
            Any exception that occurred in the with block
        """
        if exc_type is not None:
            raise exc_type(exc_val).with_traceback(exc_tb)
        
        return True


class RedisDatabase:
    """Redis Database client"""
    
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def blacklist_token(self, token: str, ttl_s: int) -> bool:
        """
        Add token to the redis blacklist
        
        Args:
            token(str): token
            ttl_s (int): Time remaining for token to expire in seconds
        
        Returns:
            bool: True if token is successfully blacklisted, False otherwise
        """
        try:
            with RedisClient() as client:
                client.setex(
                    f"blacklist_token:{token}",
                    ttl_s,
                    "revoked"
                )
                return True
        
        except Exception as ex:
            log.actions.error(f"Error blacklisting token {token}: {str(ex)}")
            return False


class User(DeclarativeBase):
    """User model for SQLAlchemy ORM"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=True)
    middle_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False)


class MySQLSession:
    """Database session manager"""
    
    __engine = None
    __SessionLocal = None
    
    @classmethod
    def _get_engine(cls):
        """Get or create SQLAlchemy engine"""
        if cls.__engine is None:
            database_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
            cls.__engine = create_engine(database_url, pool_pre_ping=True, echo=False)
        return cls.__engine
    
    @classmethod
    def check_access(cls) -> bool:
        """
        Checks connection to MySQL database
        
        :return: bool indicating connection status
        """
        try:
            engine = cls._get_engine()
            with engine.connect() as connection:
                connection.execute(alc.text("SELECT 1"))
            log.actions.info("MySQL database connection successful")
            return True

        except SQLAlchemyError as e:
            log.actions.error(f"MySQL connection failed: {str(e)}")
            return False
    
    @classmethod
    def _get_session_local(cls):
        """Get or create SessionLocal factory"""
        if cls.__SessionLocal is None:
            cls.__SessionLocal = sessionmaker(bind=cls._get_engine(), class_=Session, expire_on_commit=False)
        return cls.__SessionLocal
    
    @classmethod
    def get_session(cls) -> Session:
        """Get a new database session"""
        SessionLocal = cls._get_session_local()
        return SessionLocal()
    
    @classmethod
    def init_db(cls) -> bool:
        """Initialize database tables"""
        engine = None
        try:
            engine = cls._get_engine()
            DeclarativeBase.metadata.create_all(bind=engine)
            log.actions.info("Database tables initialized successfully")
            return True
    
        except SQLAlchemyError as e:
            log.actions.error(f"Failed to initialize database: {str(e)}")
            return False
    
        finally:
            if engine is not None:
                engine.dispose()
    
    def __enter__(self):
        """
        Enter context manager and return session.
        
        Returns:
            Session: Database session instance for use in with statement
        """
        self._session = MySQLSession.get_session()
        return self._session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context manager and handle transactions.
        
        Args:
            exc_type: Exception type if exception occurred, None otherwise
            exc_val: Exception value if exception occurred, None otherwise  
            exc_tb: Exception traceback if exception occurred, None otherwise
            
        Returns:
            bool: False to propagate exception, None otherwise
        """
        try:
            if exc_type is not None:
                log.actions.error(f"Database operation error: {exc_type.__name__}: {str(exc_val)}")
                if self._session:
                    self._session.rollback()
            else:
                if self._session:
                    self._session.commit()
        
        except Exception as ex:
            log.actions.error(f"Error during transaction commit/rollback: {str(ex)}")
            if self._session:
                self._session.rollback()
        
        finally:
            if self._session:
                self._session.close()
        
        return False


class MySQLDatabase:
    """MySQL Database operations class"""
    
    __instance = None
    __initialized = False
    
    @classmethod
    def is_initialized(cls) -> bool:
        """
        Checks if MySQL database is initialized
        
        :return: bool indicating initialization status
        """
        return cls.__initialized
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def __init__(self) -> None:
        """
        Initializes MySQL database if it wasn't yet
        """
        if MySQLDatabase.__initialized:
            return
        
        try:
            if MySQLSession.check_access():
                if MySQLSession.init_db():
                    MySQLDatabase.__initialized = True
                    log.actions.info("MySQL Database initialized successfully")
        
        except Exception as err:
            log.actions.error(f'Failed to initialize MySQL DB: {err}')
    
    def register_user(
        self,
        username: str,
        password: str,
        first_name: str | None,
        middle_name: str | None,
        last_name: str | None
    ) -> bool:
        """
        Register a new user in the database
        
        Args:
            email: User email (must be unique)
            password: Plain text password (will be hashed)
            username: Optional username (defaults to email if not provided)
            first_name: Optional first name
            middle_name: Optional middle name
            last_name: Optional last name
        
        Returns:
            bool: True if registration successful, False otherwise
        """
        
        try:
            with MySQLSession() as session:
                existing_user = session.execute(
                    select(User).where(
                        (User.username == username) | (User.username == username)
                    )
                ).scalar_one_or_none()
                
                if existing_user:
                    log.actions.warning(f"User already exists: {username}")
                    return False

                password_hash = PasswordHasher().hash(password)

                new_user = User(
                    username=username,
                    password_hash=password_hash,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    is_active=True
                )
                
                session.add(new_user)
                log.actions.info(f"User registered successfully: {username}")
                return True
            
        except Exception as ex:
            log.actions.error(f"User registration failed: {ex}")
            return False
        
        # session = None
        
        # try:
        #     session = MySQLSession.get_session()
                        
        #     # Check if user already exists
        #     existing_user = session.execute(
        #         select(User).where(
        #             (User.username == username) | (User.username == username)
        #         )
        #     ).scalar_one_or_none()
            
        #     if existing_user:
        #         log.actions.warning(f"User already exists: {username}")
        #         return False
            
        #     # Hash password
        #     password_hash = ph.hash(password)
            
        #     # Create new user
        #     new_user = User(
        #         username=username,
        #         password_hash=password_hash,
        #         first_name=first_name,
        #         middle_name=middle_name,
        #         last_name=last_name,
        #         is_active=True
        #     )
            
        #     session.add(new_user)
        #     session.commit()
            
        #     log.actions.info(f"User registered successfully: {username}")
        #     return True
            
        # except IntegrityError as e:
        #     if session:
        #         session.rollback()
        #     log.actions.error(f"User registration failed - integrity error: {str(e)}")
        #     return False
        
        # except SQLAlchemyError as e:
        #     if session:
        #         session.rollback()
        #     log.actions.error(f"User registration failed - database error: {str(e)}")
        #     return False
        
        # except Exception as e:
        #     if session:
        #         session.rollback()
        #     log.actions.error(f"User registration failed - unexpected error: {str(e)}")
        #     return False
        
        # finally:
        #     if session:
        #         session.close()
    
    
    def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve user by email
        
        Args:
            email: User email
        
        Returns:
            User object if found, None otherwise
        """
        session = None
        try:
            session = MySQLSession.get_session()
            user = session.execute(
                select(User).where(User.email == email)
            ).scalar_one_or_none()
            return user
        
        except SQLAlchemyError as e:
            log.actions.error(f"Error retrieving user: {str(e)}")
            return None
        
        finally:
            if session:
                session.close()
    
    def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve user by ID
        
        Args:
            user_id: User ID
        
        Returns:
            User object if found, None otherwise
        """
        # session = None
        # try:
        #     session = MySQLSession.get_session()
        #     user = session.execute(
        #         select(User).where(User.id == user_id)
        #     ).scalar_one_or_none()
        #     return user
        
        # except SQLAlchemyError as e:
        #     log.actions.error(f"Error retrieving user: {str(e)}")
        #     return None
        
        # finally:
        #     if session:
        #         session.close()
    
    def verify_password(self, plain_password: str, password_hash: str) -> bool:
        """
        Verify a plain text password against a hash
        
        Args:
            plain_password: Plain text password
            password_hash: Hashed password
        
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            PasswordHasher().verify(password_hash, plain_password)
            return True
        
        except Exception:
            return False