from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from sqlalchemy.orm import Session
from models import Games, Base, engine
from sqlalchemy import select  # added
from sqlalchemy.engine import Engine
from typing import Optional    # added


checkpoint = "distiluse-base-multilingual-cased-v2"
model = SentenceTransformer(checkpoint)

def generate_embeddings(text: str) -> list[float]:
    """
    Function generate 512-dimention embedding using SentenceTransformer
    """
    return model.encode(text).tolist()  # necessary to get list


dataset = load_dataset("FronkonGames/steam-games-dataset")

# get columns names and types
columns = dataset["train"].features
print(columns)

columns_to_keep = ["Name", "Windows", "Linux", "Mac", "About the game", "Supported languages", "Price"]

N = 40000
dataset = dataset["train"].select_columns(columns_to_keep).select(range(N))


# function that will insert the data into the table
def insert_games(engine, dataset):
    with tqdm(total=len(dataset)) as pbar:
        for i, game in enumerate(dataset):
            game_description = game["About the game"] or ""
            game_embedding = generate_embeddings(game_description)
            name, windows, linux, mac, price = game["Name"], game["Windows"], game["Linux"], game["Mac"], game["Price"]
            if name and windows and linux and mac and price and game_description:
                game = Games(
                    name=game["Name"], 
                    description=game_description[0:4096],
                    windows=game["Windows"], 
                    linux=game["Linux"], 
                    mac=game["Mac"], 
                    price=game["Price"], 
                    game_description_embedding=game_embedding
                )
                with Session(engine) as session:
                    session.add(game)
                    session.commit()
            pbar.update(1)

# insert the data into the table
insert_games(engine, dataset)

# function that will find the games similar to the given game
def find_game(
    engine: sqlalchemy.Engine, 
    game_description: str, 
    windows: Optional[bool] = None, 
    linux: Optional[bool] = None,
    mac: Optional[bool] = None,
    price: Optional[int] = None
):
    with Session(engine) as session:
        game_embedding = generate_embeddings(game_description)
    
        query = (
            select(Games)
            .order_by(Games.game_description_embedding.cosine_distance(game_embedding))
        )
        
        if price:
            query = query.filter(Games.price <= price)
        if windows:
            query = query.filter(Games.windows == True)
        if linux:
            query = query.filter(Games.linux == True)
        if mac:
            query = query.filter(Games.mac == True)
        
        result = session.execute(query, execution_options={"prebuffer_rows": True})
        game = result.scalars().first()
        
        return game
    
game = find_game(engine, "This is a game about a hero who saves the world", price=10)
print(f"Game: {game.name}")
print(f"Description: {game.description}")

game = find_game(engine, game_description="Home decorating", price=20)
print(f"Game: {game.name}")
print(f"Description: {game.description}")

# change in the filtering requirements:
game = find_game(engine, game_description="Home decorating", mac=True, price=5)
print(f"Game: {game.name}")
print(f"Description: {game.description}")