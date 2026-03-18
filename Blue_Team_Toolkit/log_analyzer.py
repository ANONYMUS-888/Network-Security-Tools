import re
import time
import os
import requests
from collections import Counter
from dotenv import load_dotenv
import argparse

# Silently load the hidden API key from the .env file
load_dotenv()
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
DISCORD_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(ip, attempts, vt_malicious):

    # Building the professional "Rich Embed" alert
    payload = {
        "content": "🚨 **CRITICAL SECURITY ALERT** 🚨",
        "embeds": [{
             "title": "SSH Brute-Force Attack Detected",
             "color": 15158332, # This is 'Security Red'
             "fields": [
                 {"name": "Attacker IP", "value": f"`{ip}`", "inline": True},
                 {"name": "Failed Attempts", "value": str(attempts), "inline": True},
                 {"name": "VirusTotal Intel", "value": f"🚨 {vt_malicious} Malicious Detections", "inline": False}
             ],
             "footer": {"text": "SOC Automation Engine v1.0 | Real-time Alerting"}
        }]
    }

    try:
        # Pushing the alert across the internet to Discord
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("    [✓] ALERT SENT: Discord notification delivered.")
    except Exception as e:
        print(f"    [-] ALERT FAILED: Could not reach Discord. {e}") 

def check_virustotal(ip):
    # If the API key wasn't found in the .env file, stop the script safely
    if not API_KEY:
        print("[-] Error: VIRUSTOTAL_API_KEY not found. Check your .env file.")
        return None

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {
        "accept": "application/json",
        "x-apikey": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)

        # HTTP 200 means the request was successful
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            malicious = stats.get('malicious', 0)
            suspicious = stats.get('suspicious', 0)

            return malicious, suspicious
        elif response.status_code == 429:
            print(f"[-] Rate limit hit for IP {ip}. We are going too fast.")
            return None
        else:
            print(f"[-] API error {response.statusa_code} for IP {ip}")
            return None

    except Exception as e:
        print(f"[-] Connection error while checking {ip}: {e}")

def analyze_auth_logs(file_path, threshold):
    # Regex pattern to match failed SSH login attempts and extract the IP
    # Example log: "Failed password for invalid user admin from 192.168.1.50 port 44566 ssh2"
    failed_login_pattern = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)")

    suspicious_ips = []

    try:
        # Open and read the log file line by line
        with open(file_path, 'r') as log_file:
            for line in log_file:
                match = failed_login_pattern.search(line)
                if match:
                    # If a match is found, append the IP address to our list
                    suspicious_ips.append(match.group(1))

        # Count how many times each IP failed to log in
        ip_counts = Counter(suspicious_ips)

        print("\n[+] --- SSH Brute Force Detection Report --- [+]")
        print(f"Alert Threshold: {threshold} failed attempts\n")

        alert_triggered = False

        # Loop through the counted IPs and check against our threshold
        for ip, count in ip_counts.items():
            if count >= threshold:
                print(f"\n[!] CRITICAL: Brute force from {ip} ({count} attempts)")

                print("    [*] Rate limiting: Sleeping 16s for VirusTotal...")
                time.sleep(16)

                # Call the VirusTotal function you added earlier
                vt_results = check_virustotal(ip)

                if vt_results:
                    malicious, suspicious = vt_results
                    if malicious > 0 or suspicious > 0:
                        # FIRE THE ALARM!
                        send_discord_alert(ip, count, malicious)

                        print(f"    [!] THREAT DETECTED: {malicious} security vendors flagged this IP as malicious!")
                    else:
                        print("    [✓] CLEAR: VirusTotal shows 0 malicious detections from this IP.")

            alerts_triggered = True

        if not alerts_triggered:
            print("[✔] No brute-force activity detected above the threshold.")

    except FileNotFoundError:
        print(f"[-] Error: The log file '{file_path}' was not found. Please check the path.")
    except Exception as e:
        print(f"[-] An unexpected error occured: {e}")

if __name__ == "__main__":
    # Setup command-line arguments so the tool can be run dynamically
    parser = argparse.ArgumentParser(description="SOC Log Analyzer: Detects SSH brute-force attacks.")
    parser.add_argument("-f", "--file", required=True, help="Path to the auth.log file")
    parser.add_argument("-t", "--threshold", type=int, default=5, help="Failed attempts required to trigger an alert (Default: 5)")

    args = parser.parse_args()

    # Run the function with the provided arguments
    analyze_auth_logs(args.file, args.threshold)
