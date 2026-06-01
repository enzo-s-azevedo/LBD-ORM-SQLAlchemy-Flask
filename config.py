import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL não está definida. Crie um arquivo .env com DATABASE_URL para conectar ao Neon."
    )


class Config:
    # Usa a URL do banco definida em `DATABASE_URL` (fornecida pelo Neon)
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
