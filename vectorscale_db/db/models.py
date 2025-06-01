from sqlalchemy import create_engine
from sqlalchemy import Integer, String, List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector
from sqlalchemy.engine import URL

# Create URL to SQLAlchemy db
db_url = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="password",
    host="localhost",
    port=5555, 
    database="similarity_search_service_db"
)

# Create engine object to connect to db
engine = create_engine(db_url)

# Create the base class for the table definition
class Base(DeclarativeBase):
    __abstract__ = True

# Create the table definition
class Images(Base):
    __tablename__ = "images"
    VECTOR_LENGTH = 512 
    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # image path - we will use it to store the path to the image file, after similarity search we can use it to retrieve the image and display it
    image_path: Mapped[str] = mapped_column(String(256))
    # image embedding - we will store the image embedding in this column, the image embedding is a list of 512 floats this is the output of the sentence transformer model
    image_embedding: Mapped[List[float]] = mapped_column(Vector(VECTOR_LENGTH))
