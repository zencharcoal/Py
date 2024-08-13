import subprocess
import sys
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def check_hosts_up(input_file, output_file):
    up_hosts = []

    # Read hosts from the input file
    with open(input_file, 'r') as file:
        hosts = [line.strip() for line in file if line.strip()]

    for host in hosts:
        try:
            command = ["rustscan", "-a", host, "--ulimit", "5000", "--"]
            logging.info(f"Scanning {host} with RustScan")
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                logging.info(f"Host {host} is up.")
                up_hosts.append(host)
            else:
                logging.info(f"Host {host} appears to be down or RustScan encountered an error.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error scanning {host}: {e}")

    # Write up hosts to the output file
    if up_hosts:
        with open(output_file, 'w') as file:
            for host in up_hosts:
                file.write(f"{host}\n")
        logging.info(f"Up hosts written to {output_file}")
        return up_hosts
    else:
        logging.warning("No up hosts found or an error occurred during scanning.")
        return []

def detailed_nmap_scan(up_hosts, rustscan_output_file):
    if not up_hosts:
        logging.info("No hosts up for detailed scan.")
        return

    # Extract the directory of the RustScan output file
    rustscan_output_dir = os.path.dirname(rustscan_output_file)
    # Create a new directory for nmap results within the same directory as the RustScan output
    nmap_output_dir = os.path.join(rustscan_output_dir, "nmap_results")
    # Ensure the nmap output directory exists
    os.makedirs(nmap_output_dir, exist_ok=True)

    for host in up_hosts:
        try:
            logging.info(f"Performing detailed Nmap scan on {host}")
            # Generate a unique output file name for each host
            detailed_output_file_name = f"detailed_scan_{host.replace('.', '_')}.txt"
            detailed_output_file_path = os.path.join(nmap_output_dir, detailed_output_file_name)
            # Modify the command to include -oN for specifying the output file path
            command = ["sudo", "nmap", "-A", "-sVC", "-O", host, "-oN", detailed_output_file_path]
            result = subprocess.run(command, capture_output=True, text=True)
            logging.info(f"Detailed Nmap scan results for {host} are written to {detailed_output_file_path}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error during detailed scan of {host}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    up_hosts = check_hosts_up(input_file, output_file)

    # The RustScan output file path is the same as the output_file path
    detailed_nmap_scan(up_hosts, output_file)

