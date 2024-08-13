import subprocess
import json
import argparse
import os
import time
import re

def run_nmap(target):
    print(f"Scanning Host: {target}\tStatus: Up with Nmap...")
    nmap_cmd = f"nmap -oX nmap_output.xml -p- -A -sV --script vulners \"{target}\""  # Enclose target in quotes
    subprocess.run(nmap_cmd, shell=True)

def parse_nmap_xml():
    while not os.path.exists('nmap_output.xml'):
        time.sleep(5)  # Wait for 5 seconds until the file appears

def extract_ips_ports():
    ips = []
    with open('nmap_output.xml') as f:
        nmap_data = f.read()

    # Extract IP addresses and open ports
    matches = re.findall(r'Host: (.*?)\tPorts: (.*?)\t', nmap_data)
    for match in matches:
        ips.append({'ip': match[0], 'ports': match[1]})

    return ips

def trigger_nuclei(ips):
    for item in ips:
        ip = item['ip']
        ports = item['ports']
        print(f"Scanning {ip} with Nmap...")
        output_file = f"nuclei_output/{ip}.json"
        nuclei_cmd = f"nuclei -t /home/charcoal/nuclei-templates/ -target {ip}:{ports} -severity high,critical -o {output_file}"
        subprocess.run(nuclei_cmd, shell=True)
        print(f"Nuclei templates completed for {ip}, results saved in {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Automated Nmap and Nuclei Scanner")
    parser.add_argument("target_directory", help="Directory containing target files")
    args = parser.parse_args()

    target_files = os.listdir(args.target_directory)
    for target_file in target_files:
        target_file_path = os.path.join(args.target_directory, target_file)
        if os.path.isfile(target_file_path):
            with open(target_file_path) as f:
                targets = f.read().splitlines()
            for target in targets:
                run_nmap(target)
                parse_nmap_xml()  # Parse Nmap XML output
                ips = extract_ips_ports()
                trigger_nuclei(ips)

if __name__ == "__main__":
    main()
