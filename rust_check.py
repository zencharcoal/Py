import subprocess
import sys
import logging

# Setup basic logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def check_hosts_up(input_file, output_file):
    up_hosts = []

    # Read hosts from the input file
    with open(input_file, 'r') as file:
        hosts = [line.strip() for line in file if line.strip()]

    for host in hosts:
        try:
            # Ensure the correct RustScan syntax, especially for the ulimit option
            command = ["rustscan", "-a", host, "--ulimit", "5000", "--"]
            logging.info(f"Scanning {host} with RustScan")
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Debugging RustScan's output
            logging.debug(f"RustScan output for {host}: {result.stdout} {result.stderr}")

            # RustScan might not explicitly say "Host is up" in stdout; adjust logic if needed
            if result.returncode == 0:  # Assuming successful execution indicates host is up
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
    else:
        logging.warning("No up hosts found or an error occurred during scanning.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        logging.error("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    check_hosts_up(input_file, output_file)

