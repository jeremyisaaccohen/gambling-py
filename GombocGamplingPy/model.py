from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///bets.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    dice_roll = Column(Integer, nullable=False)
    outcome = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Bet {self.id}>'

Base.metadata.create_all(bind=engine)
