import psutil
import socket
import requests

def is_vpn(interface_name):
    vpn_keywords = ["vpn", "tun", "tap", "ppp", "ipsec", "pptp", "l2tp", "openvpn"]
    return any(keyword in interface_name.lower() for keyword in vpn_keywords)
    
def check_internet_access():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=2)
        public_ip = response.json()['ip']
        internet_access = "Yes"
    except:
        internet_access = "No"
        public_ip = "Unavailable"
    
    print(f"Internet Access:\t{internet_access}")
    print(f"Public IP Address:\t{public_ip}")

def show_addresses(addresses):
    for address in addresses:
        if address.family == socket.AF_INET:
            print(f"\n\tIPv4 Address:\t{address.address}")
            print(f"\tNetmask:\t{address.netmask}")
            print(f"\tBroadcast:\t{address.broadcast}")
        elif address.family == socket.AF_INET6:
            print(f"\n\tIPv6 Address:\t{address.address}")
            print(f"\tNetmask:\t{address.netmask}")
            print(f"\tBroadcast:\t{address.broadcast}")
        elif address.family == psutil.AF_LINK:
            print(f"\n\tMAC Address:\t{address.address}")
            
def show_status(interface_name):
    stats = psutil.net_if_stats()
    
    if interface_name in stats:
        is_up = stats[interface_name].isup
        iface_stats = stats[interface_name]
        print(f"\tStatus:\t\t{'Up' if is_up else 'Down'}")
        print(f"\tIs VPN:\t\t{'Yes' if is_vpn(interface_name) else 'No'}")
        print(f"\tSpeed:\t\t{iface_stats.speed} Mbps")
        print(f"\tDuplex:\t\t{'Full' if iface_stats.duplex == psutil.NIC_DUPLEX_FULL else 'Half' if iface_stats.duplex == psutil.NIC_DUPLEX_HALF else 'Unknown'}")
        print(f"\tMTU:\t\t{iface_stats.mtu} bytes")

def show_io_counters(interface_name):
    io_counters = psutil.net_io_counters(pernic=True)
    
    if interface_name in io_counters:
        iface_io = io_counters[interface_name]
        print(f"\n\tBytes Sent:\t{iface_io.bytes_sent}")
        print(f"\tBytes Received:\t{iface_io.bytes_recv}")
        print(f"\tPackets Sent:\t{iface_io.packets_sent}")
        print(f"\tPackets Recv:\t{iface_io.packets_recv}")
        print(f"\tErrors In:\t{iface_io.errin}")
        print(f"\tErrors Out:\t{iface_io.errout}")
        print(f"\tDrop In:\t{iface_io.dropin}")
        print(f"\tDrop Out:\t{iface_io.dropout}")
    
def show():
    print("===== INTERFACES ENUMERATION =====\n")
    
    interfaces = psutil.net_if_addrs()
    
    check_internet_access()
    
    for interface_name, addresses in interfaces.items():
        print(f"\nInterface: {interface_name}")
        
        show_status(interface_name)
        show_io_counters(interface_name)
        show_addresses(addresses)
        
    print()