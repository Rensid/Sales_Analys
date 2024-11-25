from dotenv import load_dotenv
import os

from openai import AsyncOpenAI

load_dotenv(override=True)


DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
TEST_DB_NAME = os.environ.get('TEST_DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
REDIS_HOST = os.environ.get('REDIS_HOST')
OPENAI_KEY = os.environ.get('OPENAI_KEY')

openai_client = AsyncOpenAI(api_key=OPENAI_KEY)
