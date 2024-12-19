import threading
import time
import pickle

class ChunkInfo:
    def __init__(self, gameId, serv):
        self.game_id = gameId
        self.serv = serv
        self.chunk_id = 1
        self.frame_id = 0
        self.last_chunk = 0
        self.running = True
        self.chunk_availability = int(time.time()*1000)
        self.player_thread = None
        self.getLastChunkInfo()
        self.init()
        
    def getLastChunkInfo(self):
        lastChunkInfo = {
            "chunkId": self.chunk_id,
	        "availableSince": int(time.time()*1000 - self.chunk_availability),
	        "nextAvailableChunk": int((self.chunk_availability+1000)-time.time()*1000),
            "keyFrameId": self.frame_id,
            "nextChunkId": self.chunk_id-1,
            "endStartupChunkId": 1,
            "startGameChunkId": 2,
            "endGameChunkId": self.last_chunk,
            "duration": 1000
        }
        return lastChunkInfo
        
    def init(self):
        with open(f'replays/{self.game_id}.pkl', 'rb') as file:
            replayData = pickle.load(file)
            for i in range(1, len(replayData)):
                if '/getGameDataChunk/'+self.serv+'/'+self.game_id+'/'+str(i) in replayData:
                    self.last_chunk = i
        
            
        self.player_thread = threading.Thread(target=self.run)
        self.player_thread.start()
        
    def run(self):
        f_timer=1
        while self.running:
            time.sleep(1)
            f_timer+=1
            self.chunk_id += 1
            self.chunk_availability = int(time.time()*1000)
            if f_timer == 2:
                self.frame_id +=1
                f_timer = 0
            if self.chunk_id == self.last_chunk:
                self.stop()

    def stop(self):
        self.running = False
        self.player_thread.join()

if __name__ == "__main__":
    ci = ChunkInfo("7233925974", "EUW1")
    for i in range(10):
        print(ci.getLastChunkInfo())
        time.sleep(10)