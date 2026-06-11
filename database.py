from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexão com o PostgreSQL
# Recomenda-se extrair isso para uma variável de ambiente em produção.
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/escola"

# Cria o motor de conexão e a fábrica de sessões do SQLAlchemy.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
