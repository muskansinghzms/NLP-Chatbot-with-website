from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Define the database base
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base
db = SQLAlchemy(model_class=Base)