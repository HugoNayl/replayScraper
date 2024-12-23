import requests

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
        champion = participant.get("championName")
        role = participant.get("teamPosition", "NONE")
        team_id = participant.get("teamId")
        did_win = teams_win_map[team_id]

        participants.append({
            "champion": champion,
            "role": role,
            "team": team_id,
            "winner": did_win
        })

    return participants


# Example usage:
if __name__ == "__main__":
    # Replace with your match ID, e.g. "EUW1_1234567890"
    match_id = "MATCH_ID"

    # Replace with your actual Riot API Key
    api_key = "API_KEY"

    try:
        match_participants = get_match_details(match_id, api_key, region="europe")
        for participant_info in match_participants:
            print(participant_info)
    except Exception as e:
        print(f"Error: {e}")