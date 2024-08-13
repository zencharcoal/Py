import argparse
import subprocess

def prepend_scheme(target, scheme):
    if not target.startswith(("http://", "https://")):
        return f"{scheme}://{target}"
    return target

def run_ffuf(scheme, input_file, wordlist, output_directory):
    with open(input_file, 'r') as file:
        targets = [line.strip() for line in file]
        for target in targets:
            target = prepend_scheme(target, scheme)
            output_file = f"{output_directory}/{target.replace('://', '_').replace('/', '_')}_ffuf.csv"
            try:
                print(f"[+] Running ffuf on {target}")
                command = ["ffuf", "-w", wordlist, "-u", f"{target}/FUZZ", "-o", output_file]
                subprocess.run(command, check=True)
            except subprocess.CalledProcessError:
                print(f"[-] ffuf scanning error for {target}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Fuzzing with ffuf")
    parser.add_argument("-s", "--scheme", choices=["http", "https"], default="http", help="Scheme to use for targets (default: http)")
    parser.add_argument("-f", "--input_file", required=True, help="Input file with target URLs, one per line")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the ffuf wordlist")
    parser.add_argument("-o", "--output_directory", required=True, help="Directory to store output files")
    args = parser.parse_args()

    run_ffuf(args.scheme, args.input_file, args.wordlist, args.output_directory)

