import subprocess
import time
import requests

# --- CONFIGURATION ---
# Paste your Discord Webhook URL inside the quotes
WEBHOOK_URL = "https://discord.com/api/webhooks/1482136619611062473/6UxG9utuObV-Ei1R7niG5233AffIcqM3-ErDTBNnv0oG-rn3e0Pc21RKXZGqclFmpYrr"
CHECK_INTERVAL = 60  # How often to check the registry (in seconds)

def get_registry_state():
    """
    Queries the Windows Registry 'Run' key.
    Returns the output as a clean list of strings.
    """
    command = r'reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RUN'
    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Split the output line by line and remove empty lines
        lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
        return lines
    except Exception as e:
        print(f"[-] Error reading registry: {e}")
        return []

def send_discord_alert(new_entry):
    """
    Sends an automated alert to Discord if a new registry key is detected.
    """
    payload = {
        "content": f"🚨 **CRITICAL: New Registry Persistence Detected!** 🚨\n\n**Suspicious Entry:**\n`{new_entry}`\n\n*Investigate the endpoint immediately!*"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print("[+] Discord alert sent successfully.")
    except Exception as e:
        print(f"[-] Failed to send Discord alert: {e}")

def main():
    print("[*] Initializing Persistence Hunter (Endpoint Security Agent)...")

    # Step 1: Capture the baseline (clean state)
    baseline = get_registry_state()
    print(f"[+] Baseline captured with {len(baseline)} entries.")
    print(f"[*] Monitoring registry every {CHECK_INTERVAL} seconds. Press CTRL+C to stop.\n")

    # Step 2: Continuous monitoring loop
    while True:
        time.sleep(CHECK_INTERVAL)
        current_state = get_registry_state()

        # Step 3: Compare current state against the baseline
        for entry in current_state:
            if entry not in baseline:
                # We found a new program trying to start with Windows!
                print(f"[!] ALERT! New persistence mechanism found: {entry}")

                # Send the webhook
                send_discord_alert(entry)

                # Add the new entry to the baseline so we don't spam Discord every 60 seconds
                baseline.append(entry)

if __name__ == "__main__":
    main()
