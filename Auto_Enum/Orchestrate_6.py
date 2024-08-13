import subprocess
import os
import shutil
import configparser
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

def load_config():
    config = configparser.ConfigParser()
    config.read('tools.config')  # Adjust this path
    return config

def run_command(command, timeout=None):
    logging.info(f"Executing: {' '.join(command)}")
    try:
        if timeout:
            result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=timeout)
        else:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info("Success: " + result.stdout)
    except subprocess.TimeoutExpired:
        logging.error(f"Command timed out: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.stderr}")

def orchestrate_script(script_path, input_path, output_dir, flags):
    command = ['python3', script_path, input_path] + flags + [output_dir]
    run_command(command)

def main():
    config = load_config()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    base_output_dir = os.path.join(config['directories']['output_base_directory'], timestamp)
    os.makedirs(base_output_dir, exist_ok=True)

    # Setup and execute rust2nmap
    rust2nmap_output_dir = setup_and_execute_rust2nmap(config, base_output_dir)

    # Move detailed scans
    detailed_scans_dir = os.path.join(base_output_dir, "detailed_scans")
    os.makedirs(detailed_scans_dir, exist_ok=True)
    move_detailed_scans(rust2nmap_output_dir, detailed_scans_dir)

    # Execute other scripts with modes and schemes
    execute_scripts_with_modes_and_schemes(config, rust2nmap_output_dir, base_output_dir)

    logging.info("Orchestration complete.")

def setup_and_execute_rust2nmap(config, base_output_dir):
    rust2nmap_script = config['scripts']['rust2nmap']
    input_directory = config['directories']['input_directory']
    output_dir = os.path.join(base_output_dir, "rust2nmap")
    os.makedirs(output_dir, exist_ok=True)

    for input_file in os.listdir(input_directory):
        full_input_path = os.path.join(input_directory, input_file)
        # Check if the path is a file before proceeding
        if os.path.isfile(full_input_path):
            output_file_path = os.path.join(output_dir, f"up_hosts_{input_file}.txt")
            orchestrate_script(rust2nmap_script, full_input_path, output_file_path, [])

    return output_dir

def execute_scripts_with_modes_and_schemes(config, rust2nmap_output_dir, base_output_dir):
    with ThreadPoolExecutor() as executor:
        for script_name in ['gobuster', 'nikto', 'nuclei', 'ffuf']:
            if script_name == 'gobuster':
                execute_gobuster(config, executor, rust2nmap_output_dir, base_output_dir)
            elif script_name == 'nikto':
                execute_nikto(config, executor, rust2nmap_output_dir, base_output_dir)
            elif script_name == 'nuclei':
                execute_nuclei(config, executor, rust2nmap_output_dir, base_output_dir)
            elif script_name == 'ffuf':
                execute_ffuf(config, executor, rust2nmap_output_dir, base_output_dir)

from concurrent.futures import ThreadPoolExecutor, as_completed

def execute_gobuster(config, executor, input_dir, base_output_dir):
    gobuster_script_path = config['scripts']['gobuster_auto']
    wordlist_dir = config['gobuster']['wordlist_dir']
    wordlist_dns = config['gobuster']['wordlist_dns']
    modes = ['dir', 'dns']
    schemes = ['http', 'https']

    def gobuster_scan(mode, scheme, input_file, wordlist, output_dir):
        input_filename = os.path.splitext(os.path.basename(input_file))[0]
        specific_output_dir = os.path.join(output_dir, f"gobuster_{mode}_{scheme}", input_filename)
        os.makedirs(specific_output_dir, exist_ok=True)
        output_file = os.path.join(specific_output_dir, f"{input_filename}_{mode}_{scheme}.txt")
        command = ['python3', gobuster_script_path, mode, '-s', scheme, '-f', input_file, '-w', wordlist, '-o', output_file]
        run_command(command)

    with ThreadPoolExecutor() as executor:
        futures = []
        for input_file in os.listdir(input_dir):
            if not input_file.startswith("up_hosts_"): continue
            input_path = os.path.join(input_dir, input_file)
            for mode in modes:
                wordlist = wordlist_dir if mode == 'dir' else wordlist_dns
                for scheme in schemes:
                    futures.append(executor.submit(gobuster_scan, mode, scheme, input_path, wordlist, base_output_dir))

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()  # You can handle results or exceptions here
            except Exception as exc:
                print(f'Generated an exception: {exc}')

def execute_nikto(config, executor, input_dir, base_output_dir):
    nikto_script_path = config['scripts']['nikto_auto']
    schemes = ['http', 'https']

    def nikto_scan(scheme, input_file, output_dir):
        output_directory = os.path.join(output_dir, f"nikto_{scheme}")
        os.makedirs(output_directory, exist_ok=True)  # Ensure the output directory exists
        command = ['python3', nikto_script_path, '-s', scheme, '-f', input_file, '-o', output_directory]
        # Utilize run_command with a specified timeout for Nikto
        run_command(command, timeout=300)

    with ThreadPoolExecutor() as executor:
        futures = []
        for input_file in os.listdir(input_dir):
            if not input_file.startswith("up_hosts_"): continue
            input_path = os.path.join(input_dir, input_file)
            for scheme in schemes:
                # Executor submits nikto_scan to run with the provided scheme and paths
                futures.append(executor.submit(nikto_scan, scheme, input_path, base_output_dir))

    # Wait for all futures to complete and handle potential exceptions
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as exc:
            logging.error(f'Generated an exception: {exc}')

def execute_nuclei(config, executor, input_dir, base_output_dir):
    nuclei_script_path = config['scripts']['nuclei_loop']
    # Assuming `workflows_dir` is a new configuration pointing to the directory containing Nuclei workflows
    workflows_dir = config['nuclei']['workflows_dir']
    schemes = ['http', 'https']

    def nuclei_scan(input_file, scheme):
        # Adjusting the output directory structure to accommodate scheme-based organization
        output_directory = os.path.join(base_output_dir, "nuclei_results", scheme)
        os.makedirs(output_directory, exist_ok=True)
        
        # This example assumes the script can take a directory or specific workflow files
        command = ['python3', nuclei_script_path, '-f', input_file, '-W', workflows_dir, '-o', output_directory, '-s', scheme]
        run_command(command)
    
    futures = []
    with ThreadPoolExecutor() as executor:
        for input_file in os.listdir(input_dir):
            if not input_file.startswith("up_hosts_"): continue
            input_path = os.path.join(input_dir, input_file)
            for scheme in schemes:
                futures.append(executor.submit(nuclei_scan, input_path, scheme))
    
    # Wait for all futures to complete
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as exc:
            logging.error(f'Generated an exception: {exc}')

def execute_ffuf(config, executor, input_dir, base_output_dir):
    ffuf_script_path = config['scripts']['ffuf_auto']
    wordlist = config['ffuf']['wordlist']
    schemes = ['http', 'https']

    def ffuf_scan(scheme, input_file, output_dir):
        output_directory = os.path.join(output_dir, f"ffuf_{scheme}")
        os.makedirs(output_directory, exist_ok=True)  # Ensure the output directory exists
        command = ['sudo', 'python3', ffuf_script_path, '-s', scheme, '-f', input_file, '-w', wordlist, '-o', output_directory]
        run_command(command)

    with ThreadPoolExecutor() as executor:
        futures = []
        for input_file in os.listdir(input_dir):
            if not input_file.startswith("up_hosts_"): continue
            input_path = os.path.join(input_dir, input_file)
            for scheme in schemes:
                futures.append(executor.submit(ffuf_scan, scheme, input_path, base_output_dir))

        # Wait for all futures to complete
        for future in as_completed(futures):
            try:
                future.result()  # Handle results or exceptions as needed
            except Exception as exc:
                print(f'Generated an exception: {exc}')

def move_detailed_scans(source_dir, target_dir):
    for file in os.listdir(source_dir):
        if file.startswith("detailed_"):
            shutil.move(os.path.join(source_dir, file), os.path.join(target_dir, file))

if __name__ == "__main__":
    main()

