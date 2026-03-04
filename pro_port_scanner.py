import socket
import argparse
import concurrent.futures
import sys
from datetime import datetime

def scan_port(target, port, timeout=1.0):
    """
    Attempts to connect to a specific port on the target.
    Returns the port number if open, otherwise None.
    """
    try:
        # Create a socket object (IPv4, TCP)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                return port
    except Exception:
        pass
    return None

def main():
    # 1. Setup Argument Parsing
    parser = argparse.ArgumentParser(description="Pro Multithreaded Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP address or hostname")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Number of concurrent threads (default: 100)")

    args = parser.parse_args()
    target_ip = socket.gethostbyname(args.target)

    print("-" * 50)
    print(f"[*] Target      : {target_ip}")
    print(f"[*] Port Range  : {args.start} - {args.end}")
    print(f"[*] Threads     : {args.workers}")
    print(f"[*] Scan Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    open_ports = []

    # 2. Execute Multithreaded Scan
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            # Map the scan_port function to the range of ports
            futures = {executor.submit(scan_port, target_ip, port): port for port in range(args.start, args.end + 1)}

            for future in concurrent.futures.as_completed(futures):
                port = futures[future]
                result = future.result()
                if result:
                    print(f"[+] Port {result:5} is OPEN")
                    open_ports.append(result)

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Exiting...")
        sys.exit(1)

    # 3. Final Report
    print("-" * 50)
    print(f"[*] Scan Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Total Open Ports Found: {len(open_ports)}")
    print("-" * 50)

if __name__ == "__main__":
    main() 
