import numpy as np
from sqlalchemy.orm import Session

from queries import (
    engine,
    insert_image,
    find_k_images,
    find_images_with_similarity_score_greater_than
)
from models import Images


def main() -> None:
    # Insert N sample image embeddings into the database
    N = 100
    for i in range(N):
        image_path = f"image_{i}.jpg"
        image_embedding = np.random.rand(512).tolist()
        insert_image(engine, image_path, image_embedding)

    # Select the first image from the database
    with Session(engine) as session:
        image = session.query(Images).first()

    if image is None:
        print("No images found in the database.")
        return

    # Find the k most similar images to the selected image
    k = 10
    similar_images = find_k_images(engine, k, image)

    print(f"\nTop {k} most similar images:")
    for sim in similar_images:
        print(f"ID: {sim.id}, Path: {sim.image_path}")

    # Find images with similarity score greater than 0.9
    similar_threshold_images = find_images_with_similarity_score_greater_than(engine, 0.9, image)

    print(f"\nImages with similarity > 0.9:")
    for sim in similar_threshold_images:
        print(f"[>0.9] ID: {sim.id}, Path: {sim.image_path}")


if __name__ == "__main__":
    main()
