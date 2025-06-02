from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from models import Images
import numpy as np
from typing import List

# reusable function to insert data into the table
def insert_image(engine: Engine, image_path: str, image_embedding: list[float]):
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

# calculate the cosine similarity between the first image and the K rest of the images, 
# order the images by the similarity score
def find_k_images(engine: Engine, k: int, orginal_image: Images) -> list[Images]:
    with Session(engine) as session:
        # execution_options={"prebuffer_rows": True} is used to prebuffer the rows, 
        # this is useful when we want to fetch the rows in chunks and return them after session is closed
        result = session.execute(
            select(Images)
            .order_by(Images.image_embedding.cosine_similarity(orginal_image.image_embedding))
            .limit(k), 
            execution_options={"prebuffer_rows": True}
        )
        return [row[0] for row in result]   # Return a list of objects instead of a Result object

# find the images with the similarity score greater than 0.9
def find_images_with_similarity_score_greater_than(engine: Engine, similarity_score: float, orginal_image: Images) -> list[Images]:
    with Session(engine) as session:
        result = session.execute(
            select(Images)
            .filter(Images.image_embedding.cosine_similarity(orginal_image.image_embedding) > similarity_score), 
            execution_options={"prebuffer_rows": True}
        )
        return [row[0] for row in result]
