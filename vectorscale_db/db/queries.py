from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import engine, Images
import numpy as np

# reusable function to insert data into the table
def insert_image(engine: sqlalchemy.Engine, image_path: str, image_embedding: list[float]):
    with Session(engine) as session:
        # create the image object
        image = Images(
            image_path=image_path,
            image_embedding=image_embedding
        )
        # add the image object to the session
        session.add(image)
        # commit the transaction
        session.commit()

# insert some data into the table
N = 100
for i in range(N):
    image_path = f"image_{i}.jpg"
    image_embedding = np.random.rand(512).tolist()
    insert_image(engine, image_path, image_embedding)

# select first image from the table
with Session(engine) as session:
    image = session.query(Images).first()


# calculate the cosine similarity between the first image and the K rest of the images, 
# order the images by the similarity score
def find_k_images(engine: sqlalchemy.Engine, k: int, orginal_image: Images) -> list[Images]:
    with Session(engine) as session:
        # execution_options={"prebuffer_rows": True} is used to prebuffer the rows, 
        # this is useful when we want to fetch the rows in chunks and return them after session is closed
        result = session.execute(
            select(Images)
            .order_by(Images.image_embedding.cosine_similarity(orginal_image.image_embedding))
            .limit(k), 
            execution_options={"prebuffer_rows": True}
        )
        return result

# find the 10 most similar images to the first image
k = 10
similar_images = find_k_images(engine, k, image)

# optional path to similar images
for sim in similar_images:
    print(f"ID: {sim.id}, Path: {sim.image_path}")
