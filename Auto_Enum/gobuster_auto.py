import argparse
import subprocess

def run_gobuster(mode, scheme, input_file, wordlist, output_file):
    with open(input_file, 'r') as file:
        for line in file:
            target = line.strip()
            if mode == "dir" and not target.startswith(("http://", "https://")):
                target = f"{scheme}://{target}"
            try:
                print(f"[+] Running Gobuster in {mode} mode on {target}")
                command = ["gobuster", mode] + (["-u", target] if mode == "dir" else ["-d", target]) + ["-w", wordlist, "-o", f"{output_file}_{target.replace('://', '_').replace('/', '_')}.txt"]
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"[-] Gobuster scanning error for {target}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Enumeration with Gobuster")
    parser.add_argument("mode", choices=["dir", "dns"], help="Gobuster mode (dir/dns)")
    parser.add_argument("-s", "--scheme", choices=["http", "https"], default="http", help="Scheme for dir mode (default: http)")
    parser.add_argument("-f", "--input_file", required=True, help="Input file with targets, one per line")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to Gobuster wordlist")
    parser.add_argument("-o", "--output", required=True, help="Output file prefix for results")
    args = parser.parse_args()

    run_gobuster(args.mode, args.scheme, args.input_file, args.wordlist, args.output)

