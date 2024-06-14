from tqdm import tqdm
import nmap
import netifaces as ni
import socket
import misc
import tools.files as files

http_hosts = []

def get_active_ip_addresses():
    """
    Get all active ip addresses in your network.
    
    This function performs an 
    
    Returns:
    A list of active IP addresses (as strings) or None if no active IP addresses are found or an error occurs.
    """

    # List to store active ips
    active_ips = []

    try:
        # Get interfaces
        interfaces = ni.interfaces()
        
        # Filter interfaces only to get interfaces that are working
        interfaces = [iface for iface in interfaces if iface != 'lo']

        # Loop over working interfaces
        for interface in interfaces:

            # For each interface get the IPV4 addresses
            addresses = ni.ifaddresses(interface).get(socket.AF_INET)

            # If at least one address exists
            if addresses:
                
                # Loop over addresses to get the information
                for address_info in addresses:
                    # If there is an addr (IP) continue
                    if 'addr' in address_info:
                        # Get IP
                        ip = address_info['addr']
                        
                        # Add it to the active ips
                        active_ips.append(ip)

        # Return the active ips or None if there are no active ips
        return active_ips if active_ips else None
    
    # Catch any error and print the error
    except Exception as e:
        print(f"Error getting IP addresses: {e}")
        return None

def scan_networks(ip_addresses):
    """
    Scans a list of IP addresses for active devices and collects detailed information about each device.

    This function uses the Nmap library to perform a network scan on the provided list of IP addresses. It first discovers
    active hosts and then scans these hosts for open ports, services, and operating system information. Progress is
    visually tracked using tqdm progress bars.

    Parameters:
    ip_addresses (list of str): A list of IP addresses to scan. Each IP address should be in string format.

    Prints:
    Detailed information about each active device, including status, hostname, MAC address, operating system, and open ports.
    If no active devices are found or an error occurs, appropriate messages are printed.

    Exceptions:
    - nmap.PortScannerError: Caught if there is an error during the Nmap scanning process.
    - Exception: Caught for any other unexpected errors that occur during execution.
    """
    
    # Check if IP Addresses are Provided
    if not ip_addresses:
        return

    try:
        # Initialize Nmap Scanner
        nm = nmap.PortScanner()

        # Prepare List for Found Devices
        devices_found = []

        # First Progress Bar - Network Scanning
        with tqdm(total=len(ip_addresses), desc="Scanning network", unit="IP") as pbar:
            for ip in ip_addresses:
                pbar.set_description(f"Scanning network for {ip}")
                nm.scan(hosts=f"{ip}/24", arguments="-T5 -sP")

                for host in nm.all_hosts():
                    if host not in devices_found:
                        devices_found.append(host)
                        pbar.update(1)

        pbar.close()

        # Second Progress Bar - Device Scanning
        with tqdm(total=len(devices_found), desc="Scanning devices", unit="device") as pbar_devices:
            for host in devices_found:
                pbar_devices.set_description(f"Scanning {host}")
                nm.scan(hosts=host, arguments="-T5 -O -sV")

                for _host in nm.all_hosts():
                    print(f"\n\tStatus: {nm[_host].state()}")
                    print(f"\tHostname: {nm[_host].hostname() if nm[_host].hostname() else 'Unknown'}")

                    if 'addresses' in nm[_host] and 'mac' in nm[_host]['addresses']:
                        mac_address = nm[_host]['addresses']['mac'].upper()
                        print(f"\tMAC Address: {mac_address}")
                        
                    if 'osmatch' in nm[_host]:
                        os_match = nm[_host]['osmatch']
                        for os in os_match:
                            print(f"\tOS Name: {os['name']}")
                            print(f"\tOS Accuracy: {os['accuracy']}")

                    if nm[_host].all_protocols():
                        for protocol in nm[_host].all_protocols():
                            print(f"\tProtocol: {protocol}")

                            port_info = nm[_host][protocol]
                            sorted_ports = sorted(port_info.keys())
                            
                            for port in sorted_ports:
                                state = port_info[port]['state']
                                service = port_info[port]['name']
                                version = port_info[port]['version']
                                type = get_port_type(port)
                                print(f"\t{type}\tPort: {port}\tState: {state}\tService: {service} {version if version else ''}")
                                detect_http_service(host, port)

                pbar_devices.update(1)

        pbar_devices.close()
        
        misc.hosts_html_output(devices_found)

    # Exception Handling
    except nmap.PortScannerError as e:
        print(f"Nmap error: {e}")

    except Exception as e:
        print(f"Error scanning network: {e}")
        
def get_port_type(port: int):
    insecure_ports = [21, 23, 25, 80, 110, 143, 389, 445, 1433, 3306, 3389, 8000]
    return 'INSEC' if port in insecure_ports else ''
        
def detect_http_service(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip, port))
        s.send(b'GET / HTTP/1.0\r\n\r\n')
        banner = s.recv(1024)
        s.close()
        
        if b'HTTP' in banner:
            if b'HTTPS' in banner or port == 443:
                http_hosts.append((ip, port, 'https'))
            else:
                http_hosts.append((ip, port, 'http'))
        
    except (socket.timeout, socket.error):
        return False
        
def show():
    """
    Enumerate and display active network hosts.

    This function prints a header indicating the start of the network hosts enumeration process.
    It retrieves active IP addresses by calling `get_active_ip_addresses()` and prints them.
    If active IP addresses are found, it proceeds to scan these networks using the `scan_networks` function.
    If no active IP addresses are found, it prints a message indicating that no active IP addresses were detected.

    Steps:
    1. Prints a header for the network hosts enumeration.
    2. Calls `get_active_ip_addresses()` to retrieve active IP addresses.
    3. If active IP addresses are found:
    - Prints each active IP address.
    - Calls `scan_networks` to scan the networks of the found IP addresses.
    4. If no active IP addresses are found, prints a message indicating the lack of active IP addresses.

    Side Effects:
    - Outputs information about active IP addresses and network scanning status to the console.

    See Also:
    - `get_active_ip_addresses`: Function expected to return a list of active IP addresses.
    - `scan_networks`: Function expected to scan the networks of the provided IP addresses.
    """

    print("===== NETWORK HOSTS ENUMERATION =====\n")
    
    active_ip_addresses = get_active_ip_addresses()

    if active_ip_addresses:
        print("Active IP addresses:")
        for ip in active_ip_addresses:
            print(f"- {ip}")
        print()
        
        scan_networks(active_ip_addresses)
        
        if http_hosts:
            files.show(http_hosts)
    else:
        print("No active IP addresses found with connection.")