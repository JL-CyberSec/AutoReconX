import subprocess
import requests
import os
import re

def run_dirb(target_url):
    """
    Run the dirb command on the specified target URL using a wordlist, and return the results.

    Parameters:
    target_url (str): The URL to scan with dirb.

    Returns:
    list of str: A list of lines from the dirb output that contain the results.
                 If an error occurs, the list will contain an error message.
    
    The function prompts the user for the path to a wordlist. If the provided path does not exist,
    it defaults to '/usr/share/dirb/wordlists/common.txt'. The dirb command is then run with 
    the '-S' and '-w' options to reduce verbosity and show only results. The output is captured 
    and processed to exclude directory listings.
    
    Exceptions are handled to provide meaningful error messages in case dirb is not found or 
    other issues occur.
    """

    wordlist_path = input('Enter your own wordlist path, by default /usr/share/dirb/wordlists/common.txt will be used: ')
    
    if not os.path.exists(wordlist_path):
        wordlist_path = '/usr/share/dirb/wordlists/common.txt'

    try:
        result = subprocess.run(['dirb', target_url, wordlist_path, '-S', '-w'], capture_output=True, text=True)

        if result.returncode == 0:
            output_lines = result.stdout.splitlines()
            files_found = [line.strip() for line in output_lines if not line.startswith('==> DIRECTORY:') and line.startswith('+') and 'CODE:200' in line]

            return files_found

        else:
            return [f"Error running dirb: {result.stderr}"]

    except FileNotFoundError:
        return ["dirb command not found. Please install dirb."]

    except Exception as e:
        return [f"Error: {e}"]
    
def get_metadata(url):
    """
    Retrieve and print the HTTP headers (metadata) of the specified URL.

    Parameters:
    url (str): The URL from which to retrieve metadata.

    Returns:
    None
    
    The function sends an HTTP HEAD request to the provided URL to obtain the headers.
    If the request is successful (status code 200), it prints the headers.
    If the request fails, it does not print anything or handle errors explicitly.
    
    Note: This function requires the `requests` library to be installed.
    """

    response = requests.head(url)

    if response.status_code == 200:
        for metadata in response.headers:
            print(f"\t{metadata}: {response.headers[metadata]}")
    print('\n')

def show(http_hosts):
    """
    Display active HTTP(S) hosts and enumerate public files on each host.

    Parameters:
    http_hosts (list of tuples): A list of tuples where each tuple contains:
                                 - host (str): The hostname or IP address.
                                 - port (int): The port number.
                                 - scheme (str): The URL scheme (http or https).

    Returns:
    None

    The function prints the list of active HTTP(S) hosts provided and then 
    enumerates public files on each host using the `run_dirb` function. 
    For each host, it constructs the target URL, runs `run_dirb` to find 
    public files, and prints the results.
    
    Note: This function relies on the `run_dirb` function to search for public files.
    """

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
                print(f"{line}")

                pattern = r'\+ (http://[^ ]+)'
                match = re.search(pattern, line)

                if match:
                    get_metadata(match.group(1))
