from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

app = FastAPI()

# SQLite in-memory or file DB
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./urls.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define URL map model
class URLMap(Base):
    __tablename__ = "url_map"
    short_code = Column(String, primary_key=True, index=True)
    long_url = Column(String, nullable=False)

# Create the table and populate initial data
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(URLMap).first():
        initial_data = [
            ("1", "https://www.mymax.com/test/testeer"),
            ("2", "https://dataloader.io/"),
            ("3", "https://github.com"),
            ("4", "https://https://maxcu.okta.com/app/salesforce/exk1qh5gqozPcHE6R1d8/slo/saml"),
            ("5", "https://www.reddit.com"),
            ("6", "https://docs.python.org/3/"),
            ("7", "https://salesforce.com/"),
            ("8", "https://render.com"),
            ("9", "https://azure.microsoft.com"),
            ("10", "https://stackoverflow.com"),
        ]
        for short, long in initial_data:
            db.add(URLMap(short_code=short, long_url=long))
        db.commit()
    db.close()

init_db()

# Redirect route
@app.get("/{short_code}")
def redirect_to_long_url(short_code: str):
    db = SessionLocal()
    url = db.query(URLMap).filter(URLMap.short_code == short_code).first()
    db.close()
    if url:
        return RedirectResponse(url.long_url)
    raise HTTPException(status_code=404, detail="Short URL not found")
