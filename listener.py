import socket

# Configuration
HOST = "127.0.0.1"  # Listen on all network interfaces
PORT = 2999     # Port to monitor
LOG_FILE = "tcp_log.txt"

try:
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Reuse port
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Allow up to 5 connections
        print(f"Listening for TCP connections on {HOST}:{PORT}...")

        with open(LOG_FILE, "a") as log_file:
            while True:
                # Accept an incoming connection
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                with client_socket:
                    while True:
                        data = client_socket.recv(1024)  # Receive up to 1024 bytes
                        if not data:
                            print(f"Connection closed by {addr}")
                            break
                        
                        # Decode, log, and display the data
                        decoded_data = data.decode('utf-8', errors='ignore')
                        log_file.write(f"{addr}: {decoded_data}\n")
                        log_file.flush()
                        print(f"{addr}: {decoded_data}")

except KeyboardInterrupt:
    print("\nServer stopped.")
except Exception as e:
    print(f"An error occurred: {e}")
