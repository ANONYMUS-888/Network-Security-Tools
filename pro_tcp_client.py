import socket
import argparse

# 1. Command-line arguments setup
parser = argparse.ArgumentParser(description="Professional TCP Client - Security Tool")
parser.add_argument("-t", "--target", required=True, help="Target IP address or domain name")
parser.add_argument("-p", "--port", type=int, default=80, help="Target port (Default: 80)")

# 2. Parsing arguments
args = parser.parse_args()

target_host = args.target
target_port = args.port

print(f"[*] Initiating connection to {target_host}:{target_port}...")

# 3. Network connection setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((target_host, target_port))
    
    # Dynamic payload
    payload = f"GET / HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
    client.send(payload.encode())
    
    # Receiving response
    response = client.recv(4096)
    print(response.decode())

except Exception as e:
    print(f"[!] Error occurred: {e}")

finally:
    client.close()
