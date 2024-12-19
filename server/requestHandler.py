from http.server import BaseHTTPRequestHandler, HTTPServer
from server.chunkInfo import ChunkInfo
import json
import pickle
import base64

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        common_path = '/observer-mode/rest/consumer'
        req = self.path.replace(common_path, '')
        
        if req[:16] == '/getGameMetaData':
            req = req[:32]
        elif req[:17] == '/getGameDataChunk' or req[:12] == '/getKeyFrame':
            req = req[:-6]

        try:
            if req[:17] == '/getLastChunkInfo':
                self.wfile.write(json.dumps(self.chunk_info.getLastChunkInfo()).encode('utf-8'))
            else:
                with open(f'replays/{self.game_id}.pkl', 'rb') as file:
                    replayData = pickle.load(file)

                    if req in replayData:
                        res = replayData[req]
                        self.wfile.write(base64.b64decode(res))
                    else:
                        print("data not found: ", req)
                        self.send_error(404, "Data not found")

        except FileNotFoundError:
            print("file not found")
            self.send_error(500, "Pickle file not found")

        except KeyError:
            print('request key not found: ', req)
            self.send_error(404, "Requested key not found in the pickle file")

        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.chunk_info.stop()

            

# Start the server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    try:
        gameId = "7234213218"
        handler_class.game_id = gameId
        handler_class.chunk_info = ChunkInfo(gameId, "EUW1")
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print(f"Server running on http://127.0.0.1:{port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(("Stoping serv (max 30 sec)"))
        handler_class.chunk_info.stop()

if __name__ == '__main__':
    run()
