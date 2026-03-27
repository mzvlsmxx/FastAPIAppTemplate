import time

from broker import KafkaClient


def ensure_kafka_connection(timeout_s: float | None = 30.0, delay_s: float = 5.0) -> bool:
    """
    Wait for kafka connection to establish
    
    :param timeout_s: Timeout for retries in seconds. (set None for endless retrying)
    :return: True if connection is established or False otherwise
    """
    if timeout_s is None:
        try:
            while not KafkaClient.check_access():
                time.sleep(delay_s)
            return True
        except KeyboardInterrupt:
            return False
    
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < timeout_s:
        try:
            if KafkaClient.check_access():
                return True
            time.sleep(delay_s)
        except KeyboardInterrupt:
            return False
    return False