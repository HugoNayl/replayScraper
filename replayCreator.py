import requests
import base64
import time
import json
import pickle

class ReplayCreator:
    def __init__(self, gameId, serv):
        self.game_id = str(gameId)
        self.serv = serv.upper()
        
        self.base_url = f"http://spectator.{serv}.lol.pvp.net:8080/observer-mode/rest/consumer/"
        
        self.gameData = {}
        
        self.run()
        
    def get_version(self):
        try:
            response = requests.get(self.base_url + 'version')
            response.raise_for_status()
            print(response.content)
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_meta_data(self):
        try:
            response = requests.get(self.base_url + f'getGameMetaData/{self.serv}/{self.game_id}/0/token')
            response.raise_for_status()
            print(response.content)
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            
    def get_last_chunk_info(self):
        try:
            response = requests.get(self.base_url + f'getLastChunkInfo/{self.serv}/{self.game_id}/0/token')
            response.raise_for_status()
            print("chunk: ", response.json()["chunkId"])
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    def get_chunk_data(self, i):
        if i == 0:
            return
        try:
            response = requests.get(self.base_url + f'getGameDataChunk/{self.serv}/{self.game_id}/{i}/token')
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        
    def get_key_frame(self, i):
        if i == 0:
            return
        try:
            response = requests.get(self.base_url + f'getKeyFrame/{self.serv}/{self.game_id}/{i}/token')
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
#can get 5 chunk earlier
#chunk=1 loading chunk =0 doing delay chunk = 2 start of the game
    def run(self):
        self.gameData['/version'] = base64.b64encode(self.get_version())
        metaData = json.loads(self.get_meta_data().decode('utf-8'))
        metaData["gameEnded"] = True
        self.gameData['/getGameMetaData/'+self.serv+'/'+self.game_id] = base64.b64encode(json.dumps(metaData).encode('utf-8'))
        lastChunk = 0
        lastKeyFrame = 0

        #init replay
        info = self.get_last_chunk_info()
        if info["chunkId"] > 1:
            for i in range(1, info ["chunkId"]+1):
                chunk = self.get_chunk_data(i)
                if chunk:
                    self.gameData['/getGameDataChunk/'+self.serv+'/'+self.game_id+'/'+str(i)] = base64.b64encode(chunk)
                    lastChunk = i

            for i in range(1, info ["keyFrameId"]+1):
                frame = self.get_key_frame(info["keyFrameId"])
                if frame:
                    self.gameData['/getKeyFrame/'+self.serv+'/'+self.game_id+'/'+str(i)] = base64.b64encode(frame)
                    lastKeyFrame = info["keyFrameId"]
        
        while True:
            info = self.get_last_chunk_info()
            if info["chunkId"] != 0:
                #Store chunk
                if info["chunkId"] > lastChunk:
                    chunk = self.get_chunk_data(info["chunkId"])
                    if chunk:
                        self.gameData['/getGameDataChunk/'+self.serv+'/'+self.game_id+'/'+str(info["chunkId"])] = base64.b64encode(chunk)
                        lastChunk = info["chunkId"]
                
                #Store Key Frame
                if info["keyFrameId"] > lastKeyFrame:
                    frame = self.get_key_frame(info["keyFrameId"])
                    if frame:
                        self.gameData['/getKeyFrame/'+self.serv+'/'+self.game_id+'/'+str(info["keyFrameId"])] = base64.b64encode(frame)
                        lastKeyFrame = info["keyFrameId"]

                #break if final chunk stored
                print("end: ", info["endGameChunkId"])
                if info["endGameChunkId"] == info["chunkId"]:
                    break
            
            time.sleep((info["nextAvailableChunk"]/1000)+1)
        
        with open(f'{self.game_id}.pkl', 'wb') as file:
            pickle.dump(self.gameData, file)
        