import ipaddress
import sys

def is_private_ipv4(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except ValueError:
        return None  # Indicates an invalid IP address

def process_ipv4_file(input_file):
    private_ips = []
    public_ips = []

    with open(input_file, 'r') as file:
        for line in file:
            ip = line.strip()
            if is_private_ipv4(ip) is True:
                private_ips.append(ip)
            elif is_private_ipv4(ip) is False:
                public_ips.append(ip)
            # Invalid IPs are ignored

    base_name = input_file.rsplit('.', 1)[0]
    with open(f'{base_name}_private.txt', 'w') as file:
        file.write("\n".join(private_ips))
    with open(f'{base_name}_public.txt', 'w') as file:
        file.write("\n".join(public_ips))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_ipv4.py <input_file>")
        sys.exit(1)

    process_ipv4_file(sys.argv[1])

