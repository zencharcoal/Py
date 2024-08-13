import argparse
import subprocess
from urllib.parse import urlparse

def run_nikto(scheme, input_file, output_directory):
    with open(input_file, 'r') as file:
        for line in file:
            target = line.strip()
            # Validate and prepend scheme if not present
            if not urlparse(target).scheme:
                target = f"{scheme}://{target}"
            # Define output file path based on target
            output_file = f"{output_directory}/{target.replace('://', '_').replace('/', '_')}_nikto.txt"
            try:
                print(f"[+] Running Nikto on {target}")
                command = ["nikto", "-h", target, "-o", output_file,]
                subprocess.run(command, check=True)
                print(f"[+] Results saved to {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"[-] Nikto scanning error for {target}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Scanning with Nikto")
    parser.add_argument("-s", "--scheme", choices=["http", "https"], default="http", help="Scheme to use for targets (default: http)")
    parser.add_argument("-f", "--input_file", required=True, help="Input file with target URLs, one per line")
    parser.add_argument("-o", "--output_directory", required=True, help="Directory to store output files")
    args = parser.parse_args()

    run_nikto(args.scheme, args.input_file, args.output_directory)

