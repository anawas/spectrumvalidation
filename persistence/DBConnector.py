import sqlite3
import sqlalchemy
import sys
sys.path.append(".")
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
    
    def get_snr_for_file(self, filename) -> list:
        with Session(self.__engine) as session:
            statement = sqlalchemy.select(ValidationResult).filter_by(filename=filename)
            return session.execute(statement).all()

    def entry_exists(self, filename) -> bool:
        result = self.get_snr_for_file(filename)
        if len(result) == 0:
            return False
        return True
            

if __name__ == "__main__":
    con = DBConnector()
    if con.entry_exists("Arecibo-Observatory_20220202_1703_1854.fit.gz"):
        print("File already processed -> skipped")
    else:
        print("Processing file")
