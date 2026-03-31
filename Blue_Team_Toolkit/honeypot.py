import socket
import requests
from datetime import datetime

# --- CONFIGURATION ---
# Insert your Discord Webhook URL here
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"
# The port we open as a trap (Using 2222 so we don't need Admin privileges to run the test)
HONEYPOT_PORT = 2222

def send_discord_alert(attacker_ip):
    """Sends an automated alert to Discord with the attacker's IP address."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "content": f":rotating_light: **HONEYPOT ALERT!** :rotating_light:\n\n"
                   f"**Unauthorized Connection Attempt Detected!**\n"
                   f"**Attacker IP:** `{attacker_ip}`\n"
                   f"**Target Port:** `{HONEYPOT_PORT}`\n"
                   f"**Timestamp:** `{timestamp}`\n\n"
                   f"*Immediate endpoint investigation reccomended.*"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print(f"[+] Discord alert sent successfully for IP: {attacker_ip}")
    except Exception as e:
        print(f"[-] Failed to send Discord alert: {e}")

def start_honeypot():
    """Initializes the honeypot and listens for incoming connections."""
    # Create a TCP network socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", HONEYPOT_PORT))
    server.listen(5)

    print(f"[*] Honeypot is active. Listening on port {HONEYPOT_PORT}...")
    print(f"[*] Waiting for network scanners or attackers...\n")

    while True:
        try:
            # Accept the connection and capture the attacker's IP
            client_socket, client_address = server.accept()
            attacker_ip = client_address[0]

            print(f"[!] INTRUSION ATTEMPT DETECTED from IP: {attacker_ip}")

            # Send a fake SSH banner to deceive automated network scanners
            fake_banner = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n"
            client_socket.send(fake_banner)

            # Drop the connection immediately (Do not let them into the system)
            client_socket.close()

            # Trigger the Discord Webhook alert
            send_discord_alert(attacker_ip)

        except KeyboardInterrupt:
           print("\n[*] Honeypot shut down manually (Ctrl+C).")
           break
        except Exception as e:
           print(f"[-] An error occurred: {e}")

if __name__ == "__main__":
    start_honeypot() 
