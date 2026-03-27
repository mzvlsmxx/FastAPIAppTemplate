import time

from database import MySQLClient, RedisClient


def ensure_db_connection(timeout_s: float | None = 30.0, delay_s: float = 5.0) -> bool:
    """
    Wait for DB connection to establish
    
    :param timeout_s: Timeout for retries in seconds. (set None for endless retrying)
    :return: True if connection is established or False otherwise
    """
    if timeout_s is None:
        try:
            while not (MySQLClient.check_access() and RedisClient.check_access()):
                time.sleep(delay_s)
            return True
        except KeyboardInterrupt:
            return False
    
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < timeout_s:
        try:
            if MySQLClient.check_access() and RedisClient.check_access():
                return True
            time.sleep(delay_s)
        except KeyboardInterrupt:
            return False
    return False


def ensure_mysql_connection(timeout_s: float | None = 30.0, delay_s: float = 5.0) -> bool:
    """
    Wait for DB connection to establish
    
    :param timeout_s: Timeout for retries in seconds. (set None for endless retrying)
    :return: True if connection is established or False otherwise
    """
    if timeout_s is None:
        try:
            while not MySQLClient.check_access():
                time.sleep(delay_s)
            return True
        except KeyboardInterrupt:
            return False
    
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < timeout_s:
        try:
            if MySQLClient.check_access():
                return True
            time.sleep(delay_s)
        except KeyboardInterrupt:
            return False
    return False


def ensure_redis_connection(timeout_s: float | None = 30.0, delay_s: float = 5.0) -> bool:
    """
    Wait for DB connection to establish
    
    :param timeout_s: Timeout for retries in seconds. (set None for endless retrying)
    :return: True if connection is established or False otherwise
    """
    if timeout_s is None:
        try:
            while not RedisClient.check_access():
                time.sleep(delay_s)
            return True
        except KeyboardInterrupt:
            return False
    
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < timeout_s:
        try:
            if RedisClient.check_access():
                return True
            time.sleep(delay_s)
        except KeyboardInterrupt:
            return False
    return False