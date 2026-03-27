import os
from enum import Enum

import redis
import sqlalchemy as alc
from sqlalchemy.exc import SQLAlchemyError
import mysql.connector
from dotenv import load_dotenv, find_dotenv

import logs as log


load_dotenv(find_dotenv())


REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWD = os.getenv('MYSQL_PASSWD', 'passwd')


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
        Add JWT to the redis blacklist
        
        Args:
            token(str): JWT
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


class MySQLClient:
    """MySQL client wrapper class"""
    
    @classmethod
    def check_access(cls) -> bool:
        """
        Checks connection to MySQL database
        
        :return: bool indicating connection status
        """
        try:
            engine = alc.create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_HOST}:{MYSQL_PORT}/fastapi-app-template", pool_pre_ping=True)
        
            with engine.connect() as connection:
                connection.execute(alc.text("SELECT 1"))
            
            return True

        except SQLAlchemyError:
            return False
    
    # @classmethod
    # def check_access(cls) -> bool:
    #     """
    #     Checks connection to MySQL database
        
    #     :return: bool indicating connection status
    #     """
    #     try:
    #         connection = mysql.connector.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD)
    #         if connection.is_connected():
    #             connection.close()
    #             return True
    #         return False

    #     except mysql.connector.Error:
    #         return False


#     def __init__(self) -> None:
#         """Establishes connection to MySQL Database"""
        
#         self.connection = mysql.connector.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD)
#         self.cursor = self.connection.cursor()
    
#     def get_cursor(self):
#         return self.cursor
        
#     def __enter__(self):
#         return self.cursor
    
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.connection.commit()
#         self.cursor.close()
#         self.connection.close()

#         if exc_type is not None:
#             raise exc_type(exc_val).with_traceback(exc_tb)
        
#         return True
    


# class MySQLInitialization(Enum):
#     CREATE_DATABASE = (
#         'CREATE DATABASE IF NOT EXISTS `database_name`;'
#     )


# class MySQLDatabase():
#     """
#     VKR database wrapper class
#     """
#     __instance = None
#     __initialized = False
    
#     @classmethod
#     def is_initialized(cls) -> bool:
#         """
#         Checks if MySQL database is initialized
        
#         :return: bool indicating initialization status
#         """
#         return cls.__initialized
    
#     def __new__(cls):
#         if cls.__instance is None:
#             cls.__instance = super().__new__(cls)
#         return cls.__instance
    
#     def __init__(self) -> None:
#         """
#         Initializes MySQL database if it wasn't yet
#         """
#         if self.__initialized:
#             return
        
#         try:
#             if MySQLClient.check_access():
#                 self.initialize_db()
        
#         except Exception as err:
#             log.actions.error(f'Failed to initialize MySQL DB. ({err})')
        
#         else:
#             MySQLDatabase.__initialized = True
             
#     def initialize_db(self) -> None:
#         """
#         Creates database named vkr with all tables, triggers and procedures
#         """
#         with MySQLClient() as cursor:
            
#             # for command in MySQLInitialization:
#             #     cursor.execute(command.value)