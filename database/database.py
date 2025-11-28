import os
from enum import Enum

import redis
import mysql.connector
from dotenv import load_dotenv, find_dotenv

import logs as log


load_dotenv(find_dotenv())


redis_host = os.getenv('REDIS_HOST', '127.0.0.1')
redis_port = int(os.getenv('REDIS_PORT', 778))

mysql_host = os.getenv('MYSQL_HOST', '127.0.0.1')
mysql_port = int(os.getenv('MYSQL_PORT', 779))
mysql_user = os.getenv('MYSQL_USER', 'root')
mysql_passwd = os.getenv('MYSQL_PASSWD', 'passwd')


class RedisClient:
    """
    Redis client wrapper class
    """
    
    @classmethod
    def check_access(cls) -> bool:
        """
        Checks connection to Redis database
        
        :return: bool indicating connection status
        """
        try:
            redis.Redis(host=redis_host, port=redis_port, db=0).ping()
            return True
        
        except redis.ConnectionError:
            return False
    
    def __init__(self):
        self.client = redis.Redis(host=redis_host, port=redis_port, db=0)


class MySQLClient:
    """
    MySQL client wrapper class
    """
    @classmethod
    def check_access(cls) -> bool:
        """
        Checks connection to MySQL database
        
        :return: bool indicating connection status
        """
        try:
            connection = mysql.connector.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_passwd)
            if connection.is_connected():
                connection.close()
                return True
            return False

        except mysql.connector.Error:
            return False
    
    def __init__(self) -> None:
        """
        Establishes connection to MySQL Database
        """
        self.connection = mysql.connector.connect(host=mysql_host, port=mysql_port, user=mysql_user, passwd=mysql_passwd)
        self.cursor = self.connection.cursor()
    
    def get_cursor(self):
        return self.cursor
        
    def __enter__(self):
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

        if exc_type is not None:
            raise exc_type(exc_val).with_traceback(exc_tb)
        
        return True
    


class MySQLInitialization(Enum):
    CREATE_DATABASE = (
        'CREATE DATABASE IF NOT EXISTS `database_name`;'
    )


class MySQLDatabase():
    """
    VKR database wrapper class
    """
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
        if self.__initialized:
            return
        
        try:
            if MySQLClient.check_access():
                self.initialize_db()
        
        except Exception as err:
            log.actions.error(f'Failed to initialize MySQL DB. ({err})')
        
        else:
            MySQLDatabase.__initialized = True
             
    def initialize_db(self) -> None:
        """
        Creates database named vkr with all tables, triggers and procedures
        """
        with MySQLClient() as cursor:
            for command in MySQLInitialization:
                cursor.execute(command.value)