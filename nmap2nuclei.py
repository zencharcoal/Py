import json
import argparse
import os
import time
import subprocess

def run_nmap(target):
    nmap_cmd = f"nmap -oA nmap_output -p- -A -sV --script vulners {target}"
    subprocess.run(nmap_cmd, shell=True)

def parse_nmap_json():
    while not os.path.exists('nmap_output.json'):
        time.sleep(300)  # Wait for 5 minutes until the file appears

    with open('nmap_output.json') as f:
        nmap_data = json.load(f)

    findings = []
    for host in nmap_data['host']:
        ip = host['address'][0]['addr']
        ports = []

        if 'ports' in host:
            for port in host['ports']['port']:
                if 'service' in port:
                    service = port['service']['name']
                    ports.append({'port': port['portid'], 'service': service})

        if ports:
            findings.append({'ip': ip, 'ports': ports})

    return findings

def trigger_nuclei(findings):
    for finding in findings:
        ip = finding['ip']
        for port in finding['ports']:
            service = port['service']
            port_number = port['port']
            templates = []

            if service == 'http':
                templates = ['http-vuln-*', 'http-cors', 'http-misconfiguration']
            elif service == 'ftp':
                templates = ['ftp-*']
            # Add more conditions based on services

            if templates:
                for template in templates:
                    nuclei_cmd = f"nuclei -t {template} -target {ip}:{port_number} -o nuclei_output/{ip}_{port_number}_{template}.json"
                    subprocess.run(nuclei_cmd, shell=True)

def main():
    parser = argparse.ArgumentParser(description="Automated Nmap and Nuclei Scanner")
    parser.add_argument("target_files", nargs='+', help="Files containing lists of domains and IPs")
    args = parser.parse_args()

    for target_file in args.target_files:
        with open(target_file) as f:
            targets = f.read().splitlines()
        for target in targets:
            run_nmap(target)
            findings = parse_nmap_json()
            trigger_nuclei(findings)

if __name__ == "__main__":
    main()
