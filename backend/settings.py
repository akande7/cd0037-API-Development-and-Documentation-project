import os
from dotenv import load_dotenv

load_dotenv()

DB_URL=os.getenv("DB_URL","DEFAULT_VALUE")
DB_NAME=os.getenv("DB_NAME","DEFAULT_VALUE")
DB_USER=os.getenv("DB_USER","DEFAULT_VALUE")
DB_HOST=os.getenv("DB_HOST","DEFAULT_VALUE")
DB_PASSWORD=os.getenv("DB_PASSWORD","DEFAULT_VALUE")
DB_NAME_TEST=os.getenv("DB_NAME_TEST","DEFAULT_VALUE")