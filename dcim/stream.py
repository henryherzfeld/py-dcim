from walrus import *
from dcim.configuration import get_config


class StreamEngine:
    stream = 0

    def __init__(self):
        stream_config = get_config('db')
        host = stream_config['DB_HOST']

        db = Database(
            host=host,
            port=6379,
            db=0
        )
        self.stream = db.Stream('stream')

    def add(self, data):
        if data:
            self.stream.add(data)