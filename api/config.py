import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
