from sqlalchemy import create_engine, MetaData, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Constants
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://username:password@localhost:5432/mydatabase")  # Using environment variable

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData(bind=engine)
Base = declarative_base()

# Sample Model (you can separate this out into another module if you have multiple models)
class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(String)
    closing_price = Column(Integer)

def get_db_session():
    """Get a new database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_data(db, data_object):
    """
    Insert a new data object into the database.
    
    Parameters:
        db: Database session.
        data_object: The data object to insert.
    """
    db.add(data_object)
    db.commit()

def query_data(db, model, filter_conditions=None):
    """
    Query data from the database.
    
    Parameters:
        db: Database session.
        model: The database model/table to query from.
        filter_conditions (optional): SQLAlchemy filter conditions.
        
    Returns:
        List of queried data objects.
    """
    query = db.query(model)
    if filter_conditions:
        query = query.filter(filter_conditions)
    return query.all()

# Additional utility functions can be added as needed, such as update_data, delete_data, etc.
