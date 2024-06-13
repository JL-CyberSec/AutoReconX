import psutil
import socket

interfaces = psutil.net_if_addrs()
    
def print_network_interfaces():
    for interface_name, addresses in interfaces.items():
        print(f"\n\rInterface: {interface_name}")
        
        for address in addresses:
            if address.family == socket.AF_INET:
                print(f"\tIPv4 Address: {address.address}")
                print(f"\tNetmask: {address.netmask}")
                print(f"\tBroadcast: {address.broadcast}")
                
            elif address.family == socket.AF_INET6:
                print(f"\tIPv6 Address: {address.address}")
                print(f"\tNetmask: {address.netmask}")
                print(f"\tBroadcast: {address.broadcast}")
                
            elif address.family == psutil.AF_LINK:
                print(f"\tMAC Address: {address.address}")

if __name__ == "__main__":
    print_network_interfaces()