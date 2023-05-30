from pathlib import Path
import os

def getDataPath():
    wd = os.getcwd()
    return Path(wd) / 'data'

class PostgresCreds():
    def __init__(self) -> None:
        self.user = os.getenv('POSTGRES_USER')
        self.pw = os.getenv('POSTGRES_PW')
        self.db = os.getenv('POSTGRES_DB')
        self.host = '0.0.0.0'
        self.port = '5434'
        self.engine = f'postgresql://{self.user}:{self.pw}@{self.host}:{self.port}/{self.db}'

pg = PostgresCreds().engine
print(pg)