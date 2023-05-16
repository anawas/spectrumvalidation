import sqlite3
import sqlalchemy
from persistence.ValidationResult import Base, ValidationResult
from sqlalchemy.orm import Session

class DBConnector:
    def __init__(self) -> None:
        self.__engine = sqlalchemy.create_engine("sqlite:///validation.db", echo=True)
        Base.metadata.create_all(self.__engine)    

    def persist_snr(self, fname, burst_type, sig_to_noise):
        with Session(self.__engine) as session:
            spec = ValidationResult(
                filename=fname,
                type = burst_type,
                snr = sig_to_noise
            )
            session.add(spec)
            session.commit()

