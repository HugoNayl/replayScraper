import requests

def get_current_game(puuid, apiKey, serv):
    url = f'https://{serv}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}?api_key={apiKey}'
    try:
        response = requests.get(url)
        
        response.raise_for_status()
        
        data = response.json()
        print(data["gameId"])
        print(data["observers"]["encryptionKey"])
        return data
    except requests.exceptions.RequestException as e:
        return None

def get_puuid(name, tag, apiKey, region):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={apiKey}'
    try:
        response = requests.get(url)
        
        response.raise_for_status()
        
        data = response.json()
        print(data)
        return data["puuid"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")