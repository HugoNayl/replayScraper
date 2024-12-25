import requests
import os
import json

def get_match_details(match_id, api_key, region="europe"):
    """
    Retrieves match details from the Riot Match-V5 endpoint, parsing:
      - Champion played
      - Role (teamPosition)
      - Team ID (100 or 200)
      - Whether the participant's team won
    
    :param match_id: String ID of the match, e.g. "EUW1_1234567890"
    :param api_key: Your Riot Developer API key
    :param region: The match region for the request (default: "europe")
    :return: List of dictionaries, each representing a participant
    """
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {
        "X-Riot-Token": api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch match details. "
                        f"Status code: {response.status_code}, "
                        f"Message: {response.text}")
    
    data = response.json()
    info = data["info"]
    
    # The 'teams' array indicates which team won.
    # e.g. teams = [{"teamId": 100, "win": True, ...}, {"teamId": 200, "win": False, ...}]
    teams_data = info["teams"]
    teams_win_map = {team["teamId"]: team["win"] for team in teams_data}
    
    participants = []
    for participant in info["participants"]:
        champion = participant.get("championName").lower()
        role = participant.get("teamPosition", "NONE")
        team_id = "blue" if participant.get("teamId") == 100 else "red"
        did_win = teams_win_map[participant.get("teamId")]
        
        match role:
            case "TOP":
                role = "top"
            case "JUNGLE":
                role = "jungle"
            case "MIDDLE":
                role = "mid"
            case "BOTTOM":
                role = "adc"
            case "UTILITY":
                role = "support"

        participants.append({
            "champion": champion,
            "role": role,
            "side": team_id,
            "win": did_win
        })
    
    metadata = {
        "length": info["gameDuration"]*1000,
        "participants": participants,
        "patch": data["metadata"]["dataVersion"]
    }

    return metadata


# Example usage:
if __name__ == "__main__":
    # Replace with your match ID, e.g. "EUW1_1234567890"
    file_list = os.listdir("replayfiles")
    for file in file_list:
        game_id = file.replace(".pkl", "")
        print(game_id)
        serv = "EUW1"
        
        game_id = serv+"_"+game_id

        api_key = os.getenv("RIOT_API_KEY")

        try:
            match_details = get_match_details(game_id, api_key, region="europe")
            filename = f"{serv}_{game_id}-metadata.json"
            
            with open(filename, 'w') as metadata_file:
                json.dump(match_details, metadata_file, indent=4)
        except Exception as e:
            print(f"Error: {e}")