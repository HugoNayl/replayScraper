import game_check
from replayCreator import ReplayCreator
from metadataScraper import get_match_details

import os
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
    # set RIOT_API_KEY=API_KEY for Windows (PS: $env:RIOT_API_KEY = "API_KEY"/ export RIOT_API_KEY="API_KEY" on Unix based os
    name = "Miyamotô Musashî#EUW"
    api_key = os.getenv("RIOT_API_KEY")
    region = "europe"
    serv = 'euw1'
    key_file = 'keys.json'
    
    id = name.split('#')
    
    puuid = game_check.get_puuid(id[0], id[1], api_key, region)
    
    running = True

    while running:
        game_data = game_check.get_current_game(puuid, api_key, serv)
        if game_data is not None:
            if game_data["gameMode"] == "CLASSIC":
                game_id = game_data["gameId"]
                add_key(key_file, game_id, game_data["observers"]["encryptionKey"])
                RC = ReplayCreator(game_data["gameId"], serv)
                try:
                    match_details = get_match_details(match_id=game_id, api_key=api_key, region=region)
                    
                    filename = f"{region}_{game_id}-metadata.json"
                    
                    with open(filename, 'w') as metadata_file:
                        json.dump(match_details, metadata_file, indent=4)
                    
                except Exception as e:
                    print(f"Failed to retrieve match details for Game ID {game_id}: {e}")
        else:
            current_time = time.localtime()
            formatted_time = time.strftime("%d/%m - %H:%M", current_time)
            print(formatted_time, " - No current game found. Checking again in 60 seconds.")
        time.sleep(60) 