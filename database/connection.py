from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_URL = "postgresql://shortner:shortner@127.0.0.1:5433/shortner"

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
