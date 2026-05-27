import os


class Config:
    # Ajuste a URI conforme seu ambiente PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/projeto_orm"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
