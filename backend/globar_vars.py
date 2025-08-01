import os
import dotenv
from typing import Union
from pytz import timezone
from database import DataBase

dotenv.load_dotenv()


class Var:
    db: Union[DataBase, None] = DataBase()
    IST = timezone("Asia/Kolkata")

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365
    ACCESS_TOKEN_JWT_SUBJECT = "access"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    R_SECRET_KEY = os.environ.get('R_SECRET_KEY')
    GOOGLE_API_KEYS: list = [k.strip() for k in os.environ.get('GOOGLE_API_KEYS', '').split(' ')]
    TEST_MODE = (int(os.environ.get('TEST_MODE', 0)) == 1)
    WORKFLOW_STATUS = {}
    BASE_URL = os.environ.get('BASE_URL', 'http://localhost')