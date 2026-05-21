from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    SQLAlchemy 2.x uses a class-based declarative base.
    Every model will inherit from this class. 
    It maintains a MetaData collection of all known models.
    """
    pass