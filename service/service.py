import time

from database import MySQLClient, RedisClient
from broker import KafkaClient
import logs as log


def check_service_access() -> dict[str, str]:
    start_time: float = time.perf_counter()
    result = {
        "MySQLAccess": MySQLClient.check_access().__str__,
        "RedisAccess": RedisClient.check_access().__str__,
        "KafkaAccess": KafkaClient.check_access().__str__,
        "TimeELapsed": f'{round(time.perf_counter() - start_time, 3)}s'
    }
    log.actions.info(f'Performed a service access check')
    return result