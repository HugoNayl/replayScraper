import game_check
from replayCreator import ReplayCreator
import time


#enter the game between 3 and 5 min to have full game
if __name__ == "__main__":
    name = "Odoamne#KEKW"
    api_key = "RGAPI-eefac482-ac73-4d8f-b05f-095ec7fc4a79"
    region = "europe"
    serv = 'euw1'
    
    id = name.split('#')
    
    puuid = game_check.get_puuid(id[0], id[1], api_key, region)
    
    running = True

    while running:
        game_data = game_check.get_current_game(puuid, api_key, serv)
        if game_data is not None:
            RC = ReplayCreator(game_data["gameId"], serv)
        time.sleep(60) 