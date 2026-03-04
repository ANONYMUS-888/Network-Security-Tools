import socket
import os
import struct
import argparse

def start_sniffer(host):
    # Determine the OS (Windows needs IPPROTO_IP, Linux uses IPPROTO_ICMP for raw sniffing by default in this script)
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    try:
        # Create a raw socket and bind it to the public interface
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))

        # Include the IP headers in the captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # If using Windows, we need to send an IOCTL to set up promiscuous mode
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        print(f"[*] Sniffer started successfully. Listening on {host}...")
        print(f"[*] Waiting for packets... (Press CTRL+C to stop)\n")

        while True:
            # Read in a single packet (65535 is the max buffer size)
            raw_buffer = sniffer.recvfrom(65535)[0]

            # The first 20 bytes are the IPv4 header
            ip_header_bytes = raw_buffer[0:20]

            # Unpack the 20 bytes using the struct module
            # Format '!BBHHHBBH4s4s' maps perfectly to the 20-byte IP header structure
            iph = struct.unpack('!BBHHHBBH4s4s', ip_header_bytes)

            # Extract the Protocol (Index 6 in the unpacked tuple)
            protocol = iph[6]

            # Extract Source and Destination IP addresses (Index 8 and 9)
            # socket.inet_ntoa converts the raw 4-byte address into a readable IP string (e.g., 192.168.1.1)
            source_ip = socket.inet_ntoa(iph[8])
            dest_ip = socket.inet_ntoa(iph[9])

            print(f"[+] Packet Captured | Protocol: {protocol} | Source: {source_ip} --> Target: {dest_ip}")

    except KeyboardInterrupt:
        # Handle CTRL+C gracefully
        print("\n[*] Stopping sniffer...")

        # Turn off promiscuous mode on Windows before exiting
        if os.name == 'nt':
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    except Exception as e:
        print(f"[-] An error occured: {e}")

if __name__ == '__main__':
    # Set up the command-line arguments using argparse
    parser = argparse.ArgumentParser(description="Pro Network Sniffer - Raw Socket Implementation")
    parser.add_argument("-i", "--interface", required=True, help="The host ip address to bind to (e.g., 192.168.1.10)")

    args = parser.parse_args()

    # Start the engine
    start_sniffer(args.interface)
