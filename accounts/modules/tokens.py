import time
from secrets import token_hex


class Token:

    def __init__(self, token_ttl: int, token_size: int):
        self.token = str(token_hex(token_size))
        self.token_born = time.time()
        self.token_expire = self.token_born + token_ttl

    def __str__(self):
        return self.token


