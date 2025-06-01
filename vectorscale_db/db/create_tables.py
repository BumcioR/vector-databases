from app.db.models import Base, engine

def create_tables():
    """
    Creates tables in db
    """
    Base.metadata.create_all(engine)
    print("Tabeles created.")

if __name__ == "__main__":
    create_tables()
