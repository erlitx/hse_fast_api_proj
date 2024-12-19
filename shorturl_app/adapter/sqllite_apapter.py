from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#  Настройка 
DATABASE_URL = "sqlite:///./sqllite/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель базы данных 
class URL(Base):
    __tablename__ = "urls"

    short_id = Column(String, primary_key=True, index=True)
    full_url = Column(String, nullable=False)


# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
