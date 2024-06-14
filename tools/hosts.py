from tqdm import tqdm
import nmap
import netifaces as ni
import socket

def get_active_ip_addresses():
    active_ips = []

    try:
        interfaces = ni.interfaces()
        interfaces = [iface for iface in interfaces if iface != 'lo']

        for interface in interfaces:
            addresses = ni.ifaddresses(interface).get(socket.AF_INET)

            if addresses:
                for address_info in addresses:
                    if 'addr' in address_info:
                        ip = address_info['addr']
                        active_ips.append(ip)

        return active_ips if active_ips else None
    
    except Exception as e:
        print(f"Error getting IP addresses: {e}")
        return None

def scan_networks(ip_addresses):
    if not ip_addresses:
        return

    try:
        nm = nmap.PortScanner()

        devices_found = []

        with tqdm(total=len(ip_addresses), desc="Scanning network", unit="IP") as pbar:
            for ip in ip_addresses:
                pbar.set_description(f"Scanning network for {ip}")
                nm.scan(hosts=f"{ip}/24", arguments="-sP")

                for host in nm.all_hosts():
                    if host not in devices_found:
                        devices_found.append(host)
                        pbar.update(1)

        pbar.close()

        print()

        with tqdm(total=len(devices_found), desc="Scanning devices", unit="device") as pbar_devices:
            for host in devices_found:
                pbar_devices.set_description(f"Scanning {host}")
                nm.scan(hosts=host, arguments="-O -sV")

                for _host in nm.all_hosts():
                    print(f"\n\tStatus: {nm[_host].state()}")
                    print(f"\tHostname: {nm[_host].hostname() if nm[_host].hostname() else 'Unkwon'}")

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
                                print(f"\t\tPort: {port}\tState: {state}\tService: {service} {version if version else ''}")

                pbar_devices.update(1)
                
        pbar_devices.close()

    except nmap.PortScannerError as e:
        print(f"Nmap error: {e}")

    except Exception as e:
        print(f"Error scanning network: {e}")
        
def show():
    print("===== NETWORK HOSTS ENUMERATION =====\n")
    
    active_ip_addresses = get_active_ip_addresses()

    if active_ip_addresses:
        print("The active IP addresses are:")
        for ip in active_ip_addresses:
            print(ip)
        print()
        
        scan_networks(active_ip_addresses)
    else:
        print("No active IP addresses found with connection.")