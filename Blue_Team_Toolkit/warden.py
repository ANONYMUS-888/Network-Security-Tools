import os
import time
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- 1. CONFIGURATION (The Trap) ---
HONEY_DIR = "./honey_folder"
SUSPICIOUS_EXT = ".locked" # The extension our test ransomware will use
MALWARE_NAME = "malware.py" # The simulated malware process we will hunt

# --- 2. THE RADAR (Event Handler) ---
class RansomwareHandler(FileSystemEventHandler):

    def on_moved(self, event):
        # Triggered when ransomware renames a file after encryption
        if event.dest_path.endswith(SUSPICIOUS_EXT):
            print(f"\n[!!!] CRITICAL: Suspicious file rename detected: {event.dest_path}")
            self.trigger_defense()

    def on_modified(self, event):
        # Triggered when file content is modified
        if event.src_path.endswith(SUSPICIOUS_EXT):
            print(f"\n[!!!] CRITICAL: Encrypted file modification detected: {event.src_path}")
            self.trigger_defense()

    # --- 3. THE WEAPON (Defense Protocol) ---
    def trigger_defense(self):
        print("[*] Activating EDR Defense Protocol...")
        killed = False

        # Scan all running processes in memory (RAM)
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # If the malware's name is in the process command line
                if proc.info['cmdline'] and MALWARE_NAME in ' '.join(proc.info['cmdline']):
                    print(f"[X] Malicious process found! PID: {proc.info['pid']}")
                    print(f"[*] Executing taskkill on process...")

                    # BOOM. Kill the ransomware.
                    proc.kill()
                    killed = True
                    print("[*] Network secured. Attacker process neutralized.")

            # Error handling if process is already dead or access is denied
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if not killed:
            print("[-] Could not isolate the malicious process, but alert remains active!")

# --- 4. SYSTEM INITIALIZATION ---
def start_warden():
    # Create the Honey-folder if it doesn't exist
    if not os.path.exists(HONEY_DIR):
        os.makedirs(HONEY_DIR)
        print(f"[*] Honey-folder created: {HONEY_DIR}")

        # Create a decoy file
        with open(os.path.join(HONEY_DIR, "passwords.txt"), "w") as f:
            f.write("admin:supersecret123")

    # Setup and start the observer
    event_handler = RansomwareHandler()
    observer = Observer()
    observer.schedule(event_handler, HONEY_DIR, recursive=False)
    observer.start()

    print(f"[*] Active Ransomware Warden initialized.")
    print(f"[*] Monitoring directory: {HONEY_DIR}")
    print("[*] Waiting for attacker... (Press CTRL+C to exit)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[*] Warden shut down.")
    observer.join()

if __name__ == "__main__":
    start_warden() 
