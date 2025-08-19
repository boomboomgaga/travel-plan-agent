from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()

class APICache(Base):
    __tablename__ = "api_cache"
    id = Column(Integer, primary_key=True)
    endpoint = Column(String)
    params = Column(JSON)
    response = Column(JSON)
    cost = Column(Float)

engine = create_engine("sqlite:///cache.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def cache_response(endpoint: str, params: dict, response: dict, cost: float):
    with Session() as session:
        cache_entry = APICache(
            endpoint=endpoint,
            params=json.dumps(params),
            response=json.dumps(response),
            cost=cost
        )
        session.add(cache_entry)
        session.commit()

def get_cached_response(endpoint: str, params: dict):
    with Session() as session:
        entry = session.query(APICache).filter_by(
            endpoint=endpoint, params=json.dumps(params)
        ).first()
        return json.loads(entry.response) if entry else None
