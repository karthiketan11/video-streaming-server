import socket
import cv2
import pickle
import struct
import numpy as np
import time

# Client configuration
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(10)  # Add timeout

try:
    # Connect to the ngrok URL
    ngrok_url = input("Enter ngrok URL (tcp://x.tcp.ngrok.io): ")
    ngrok_port = int(input("Enter ngrok port: "))
    
    # Remove 'tcp://' if present in the URL
    server_addr = ngrok_url.replace("tcp://", "")
    print(f"Connecting to {server_addr}:{ngrok_port}")
    
    client_socket.connect((server_addr, ngrok_port))
    print("Connected to server")
    
    data = b""
    payload_size = struct.calcsize("Q")
    
    while True:
        try:
            # Get the message size
            while len(data) < payload_size:
                packet = client_socket.recv(4*1024)
                if not packet:
                    raise ConnectionError("Connection lost")
                data += packet
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            
            # Get the frame data
            while len(data) < msg_size:
                data += client_socket.recv(4*1024)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Display the frame
            frame = pickle.loads(frame_data)
            cv2.imshow("Client Video", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

except Exception as e:
    print(f"Connection error: {e}")

finally:
    print("Closing connection")
    client_socket.close()
    cv2.destroyAllWindows() 