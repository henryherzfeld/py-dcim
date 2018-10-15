import redis
from dcim.core import get_config


class TransactionEngine:
    connection = 0

    def __init__(self):
        config_db = get_config('db')

        host = config_db['DB_HOST']
        port = config_db['DB_PORT']
        password = config_db['DB_PASSWORD']

        self.channel = redis.Redis(
            host='host',
            port=port,
            password=password)

    def store_data(self, message):
        self.connection.publish('channel', message)