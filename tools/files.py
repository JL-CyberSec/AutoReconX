import subprocess
import requests
import os

def run_dirb(target_url):
    wordlist_path = input('Wordlist path: ')
    
    if not os.path.exists(wordlist_path):
        wordlist_path = ''

    try:
        result = subprocess.run(['dirb', target_url, wordlist_path, '-S'], capture_output=True, text=True)

        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            files_found = [line for line in output_lines if "==> DIRECTORY: " not in line]

            return files_found

        else:
            return [f"Error running dirb: {result.stderr}"]

    except FileNotFoundError:
        return ["dirb command not found. Please install dirb."]

    except Exception as e:
        return [f"Error: {e}"]
    
def get_metadata(url):
    response = requests.head(url)

    if response.status_code == 200:
        print(response.headers)

def show(http_hosts):
    print("\n===== PUBLIC FILES ENUMERATION =====\n")
    
    print("Active HTTP(S) hosts:")
    for host in http_hosts:
        print(f"- {host[0]}:{host[1]}\t{host[2]}")
    
    for host in http_hosts:
        target = f"{host[2]}://{host[0]}:{host[1]}"
        print(f"\nSearching public files in {target}:")
        results = run_dirb(target)
        
        if results:
            print("\nFound files:")
            for line in results:
                # get_metadata(line)
                print(line)
                
                
