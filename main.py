import game_check
from replayCreator import ReplayCreator
import time
import json

def add_key(file_path, gameId, key):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: {file_path}. Creating a new one.")
        data = {} 
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_path}. Overwriting it.")
        data = {} 
    
    data[gameId] = key
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

#enter the game between 3 and 5 min to have full game
if __name__ == "__main__":
    name = "Odoamne#KEKW"
    api_key = "RGAPI-eefac482-ac73-4d8f-b05f-095ec7fc4a79"
    region = "europe"
    serv = 'euw1'
    key_file = 'keys.json'
    
    id = name.split('#')
    
    puuid = game_check.get_puuid(id[0], id[1], api_key, region)
    
    running = True

    while running:
        game_data = game_check.get_current_game(puuid, api_key, serv)
        if game_data is not None:
            add_key(key_file, game_data["gameId"], game_data["observers"]["encryptionKey"])
            RC = ReplayCreator(game_data["gameId"], serv)
        time.sleep(60) 