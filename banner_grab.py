# usage: banner_grab.py list_of_hosts.txt list_of_ports.txt

import socket
import sys

def grab_banner(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((ip, port))
            s.send(b'GET / HTTP/1.1\r\nHost: ' + ip.encode() + b'\r\n\r\n')
            return s.recv(1024).decode().strip()
    except Exception as e:
        return f"Failed to connect to {ip}:{port} - {e}"

def main(ip_file, port_file):
    with open(ip_file, 'r') as file:
        ips = [line.strip() for line in file if line.strip()]

    ports = []
    with open(port_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    ports.append(int(line))
                except ValueError:
                    print(f"Warning: Skipping invalid port number '{line}'")

    for ip in ips:
        for port in ports:
            banner = grab_banner(ip, port)
            print(f"Banner for {ip}:{port}:\n{banner}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python banner_grab.py <ip_file.txt> <port_file.txt>")
        sys.exit(1)

    ip_file = sys.argv[1]
    port_file = sys.argv[2]

    main(ip_file, port_file)

