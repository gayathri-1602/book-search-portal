from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# SQLite database file (relative to project root)
DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'books.db')
DB_URL = f"sqlite:///{DB_FILE}"

# Ensure data directory exists
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String(13), unique=True)
    genre = Column(String)
    description = Column(String)
    publication_year = Column(Integer)
    publisher = Column(String)
    page_count = Column(Integer)
    language = Column(String)
    cover_url = Column(String)

    def __repr__(self):
        return f"Book({self.book_id}, '{self.title}', '{self.author}')"


def init_db():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def get_session():
    """Return a new DB session (SQLAlchemy). Remember to close it after use."""
    return SessionLocal()
