from sqlalchemy import create_engine
from utils.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_engine():
    return engine