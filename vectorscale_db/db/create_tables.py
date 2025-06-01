from db.models import Base, engine

def create_tables():
    """
    Creates tables in db:
    - images
    - games
    """
    # Dropping tables if existed
    Base.metadata.drop_all(engine)
    # Creating new ones
    Base.metadata.create_all(engine)
    print("Tabeles created (images, games).")

if __name__ == "__main__":
    create_tables()
