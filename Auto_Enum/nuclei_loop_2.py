import argparse
import subprocess

def run_nuclei_with_templates(input_file, templates, output_file, scheme):
    with open(input_file, 'r') as file:
        for line in file:
            target = f"{scheme}://{line.strip()}" if not line.strip().startswith(('http://', 'https://')) else line.strip()
            print(f"[+] Running Nuclei with templates {templates} on {target}")
            command = ["nuclei", "-u", target, "-t", templates, "-o", f"{output_file}_{target.replace('://', '_').replace('/', '_')}.txt"]
            try:
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"[-] Nuclei scanning error for {target} with templates {templates}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nuclei Scanning with Multiple Templates")
    parser.add_argument("-f", "--input_file", required=True, help="Input file with target URLs, one per line")
    parser.add_argument("-T", "--templates", required=True, help="Comma-separated list of Nuclei templates")
    parser.add_argument("-o", "--output", required=True, help="Base output file path for results")
    parser.add_argument("-s", "--scheme", required=True, choices=['http', 'https'], help="Scheme to prepend to targets")
    args = parser.parse_args()

    run_nuclei_with_templates(args.input_file, args.templates, args.output, args.scheme)

