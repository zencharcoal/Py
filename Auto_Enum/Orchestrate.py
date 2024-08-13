import subprocess
import os
import shutil
import configparser
import logging
from datetime import datetime

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

def load_config():
    config = configparser.ConfigParser()
    config.read('tools.config')  # Adjust to the correct path of your tools.config
    return config

def run_command(command):
    logging.info(f"Executing: {' '.join(command)}")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logging.info("Success: " + result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.stderr}")

def orchestrate_script(script_path, input_path, output_path, flags):
    command = ['python3', script_path, input_path, output_path] + flags
    run_command(command)

def move_detailed_scans(source_dir, target_dir):
    for file in os.listdir(source_dir):
        if file.startswith("detailed_"):
            shutil.move(os.path.join(source_dir, file), os.path.join(target_dir, file))

def main():
    config = load_config()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    base_output_dir = os.path.join(config['directories']['output_base_directory'], timestamp)
    os.makedirs(base_output_dir, exist_ok=True)

    # Directory setup for each script's output
    rust2nmap_output_dir = os.path.join(base_output_dir, "rust2nmap")
    detailed_scans_dir = os.path.join(base_output_dir, "detailed_scans")
    os.makedirs(rust2nmap_output_dir, exist_ok=True)
    os.makedirs(detailed_scans_dir, exist_ok=True)

    # Execute rust2nmap
    execute_rust2nmap(config, rust2nmap_output_dir)

    # Move detailed scans
    move_detailed_scans(rust2nmap_output_dir, detailed_scans_dir)

    # Execute other scripts with modes and schemes
    execute_gobuster(config, rust2nmap_output_dir, base_output_dir)
    execute_nikto(config, rust2nmap_output_dir, base_output_dir)
    execute_nuclei(config, rust2nmap_output_dir, base_output_dir)
    execute_ffuf(config, rust2nmap_output_dir, base_output_dir)

    logging.info("Orchestration complete.")

def execute_rust2nmap(config, output_dir):
    script_path = config['scripts']['rust2nmap']
    input_directory = config['directories']['input_directory']
    for input_file in os.listdir(input_directory):
        full_input_path = os.path.join(input_directory, input_file)
        output_path = os.path.join(output_dir, f"up_hosts_{input_file}.txt")
        orchestrate_script(script_path, full_input_path, output_path, [])

def execute_gobuster(config, input_dir, base_output_dir):
    script_path = config['scripts']['gobuster_auto']
    output_dir = os.path.join(base_output_dir, "gobuster")
    os.makedirs(output_dir, exist_ok=True)
    wordlist = config['gobuster']['wordlist_dir']
    modes = ['dir', 'dns']  # Assuming 'dir' mode; add 'dns' or others as applicable
    schemes = ['http', 'https']
    for mode in modes:
        for scheme in schemes:
            for input_file in os.listdir(input_dir):
                if not input_file.startswith("up_hosts_"): continue
                input_path = os.path.join(input_dir, input_file)
                output_file_name = f"{scheme}_{mode}_{input_file}.txt"
                output_path = os.path.join(output_dir, output_file_name)
                flags = ['-m', mode, '-s', scheme, '-w', wordlist]
                orchestrate_script(script_path, input_path, output_path, flags)

#def execute_gobuster(config, input_dir, base_output_dir):
#    script_path = config['scripts']['gobuster_auto']
#    output_dir = os.path.join(base_output_dir, "gobuster")
#    os.makedirs(output_dir, exist_ok=True)
#    wordlist = config['gobuster']['wordlist_dir']
#    modes = ['dns']  # Assuming 'dir' mode; add 'dns' or others as applicable
#    schemes = ['http', 'https']
#    for mode in modes:
#        for scheme in schemes:    
#            for input_file in os.listdir(input_dir):
#                if not input_file.startswith("up_hosts_"): continue
#                input_path = os.path.join(input_dir, input_file)
#                output_file_name = f"{scheme}_{mode}_{input_file}.txt"
#                output_path = os.path.join(output_dir, output_file_name)
#                flags = ['-m', mode, '-s', scheme, '-w', wordlist]
#                orchestrate_script(script_path, input_path, output_path, flags)

def execute_nikto(config, input_dir, base_output_dir):
    script_path = config['scripts']['nikto_auto']
    output_dir = os.path.join(base_output_dir, "nikto")
    os.makedirs(output_dir, exist_ok=True)
    for input_file in os.listdir(input_dir):
        if not input_file.startswith("up_hosts_"): continue
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, f"nikto_{input_file}.txt")
        flags = []
        orchestrate_script(script_path, input_path, output_path, flags)

def execute_nuclei(config, input_dir, base_output_dir):
    script_path = config['scripts']['nuclei_loop']
    output_dir = os.path.join(base_output_dir, "nuclei")
    os.makedirs(output_dir, exist_ok=True)
    templates = config['nuclei']['templates_dir']
    for input_file in os.listdir(input_dir):
        if not input_file.startswith("up_hosts_"): continue
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, f"nuclei_{input_file}.txt")
        flags = ['-t', templates]
        orchestrate_script(script_path, input_path, output_path, flags)

def execute_ffuf(config, input_dir, base_output_dir):
    script_path = config['scripts']['ffuf_auto']
    output_dir = os.path.join(base_output_dir, "ffuf")
    os.makedirs(output_dir, exist_ok=True)
    wordlist = config['ffuf']['wordlist']
    for input_file in os.listdir(input_dir):
        if not input_file.startswith("up_hosts_"): continue
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, f"ffuf_{input_file}.txt")
        flags = ['-w', wordlist]
        orchestrate_script(script_path, input_path, output_path, flags)

if __name__ == "__main__":
    main()

