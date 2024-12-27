import socket
import cv2
import pickle
import struct
import numpy as np
from pyngrok import ngrok
from pyngrok import conf

# Add your ngrok auth token here
ngrok.set_auth_token("2h8sq79Qc5XQuoHiwpyN5InEFkP_7nacemZ2iqpwnYucb2aFX")

# Server configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_ip = '0.0.0.0'  # Bind to all interfaces
port = 8888
socket_address = (host_ip, port)

# Bind the socket
server_socket.bind(socket_address)
server_socket.listen(5)
print(f"Listening at {socket_address}")

# Start ngrok tunnel
public_url = ngrok.connect(port, "tcp")
print(f"ngrok tunnel URL: {public_url}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    
    if client_socket:
        vid = cv2.VideoCapture(0)  # Try 0 instead of 1
        
        if not vid.isOpened():
            print("Error: Could not open video capture")
            continue
            
        while(vid.isOpened()):
            try:
                ret, frame = vid.read()
                if not ret:
                    print("Error: Can't receive frame")
                    break
                    
                frame = cv2.resize(frame, (320, 240))
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
                
                cv2.imshow('Server Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as e:
                print(f"Error during streaming: {e}")
                break
                
        vid.release()
        cv2.destroyAllWindows()
        client_socket.close()