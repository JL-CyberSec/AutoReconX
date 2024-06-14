import psutil
import socket
import requests

def is_vpn(interface_name):
    """
    Determine if the given network interface is a VPN interface.

    This function checks whether the provided network interface name contains any of the keywords typically associated 
    with VPN interfaces. It is useful for identifying VPN connections based on the interface name.

    Parameters:
    interface_name (str): The name of the network interface to check.

    Returns:
    bool: True if the interface name suggests a VPN connection, otherwise False.

    Examples:
    >>> is_vpn('tun0')
    True
    >>> is_vpn('eth0')
    False

    Notes:
    The function uses a list of keywords such as "vpn", "tun", "tap", etc., to identify VPN interfaces. It performs a case-insensitive search within the interface name.
    """

    vpn_keywords = ["vpn", "tun", "tap", "ppp", "ipsec", "pptp", "l2tp", "openvpn"]
    return any(keyword in interface_name.lower() for keyword in vpn_keywords)
    
def check_internet_access():
    """
    Check for internet access and retrieve the public IP address.

    This function attempts to determine if the system has internet access by making a request to 'https://api.ipify.org'.
    If successful, it prints the system's public IP address and confirms internet access. If the request fails, it indicates
    that internet access is not available and marks the public IP address as unavailable.

    Actions:
    1. Makes an HTTP GET request to 'https://api.ipify.org' to determine the public IP address.
    2. Sets a timeout for the request to avoid indefinite hanging in case of network issues.
    3. Based on the response:
       - If successful, prints "Yes" for internet access and the public IP address.
       - If unsuccessful, prints "No" for internet access and "Unavailable" for the IP address.

    Prints:
    - "Internet Access: Yes/No"
    - "Public IP Address: [IP address or Unavailable]"

    Exceptions:
    - Any exception during the HTTP request will set the internet access to "No" and IP address to "Unavailable".

    Requires:
    - The 'requests' library, which should be installed in the environment where this function is executed.

    Example:
    >>> check_internet_access()
    Internet Access: Yes
    Public IP Address: 192.168.1.1

    """

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
    """
    Print details of network addresses for each network interface.

    This function processes a list of network addresses and prints information based on the type of address:
    IPv4, IPv6, and MAC addresses. It uses socket families to distinguish between these address types.

    Parameters:
    addresses (list): A list of address objects, each representing network details for an interface.

    Details Printed:
    - For IPv4 addresses: IPv4 address, netmask, and broadcast address.
    - For IPv6 addresses: IPv6 address, netmask, and broadcast address.
    - For MAC addresses: MAC address.

    Example:
    >>> addresses = [...]  # This would be obtained from a network interface querying function
    >>> print_network_addresses(addresses)
    - Output will include details for each address type (IPv4, IPv6, MAC) in the list.

    """

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
    """
    Display network interface statistics.

    This function retrieves and prints various statistics about the specified network interface using the psutil library.
    It provides information such as the interface's status, speed, duplex mode, and MTU size.

    Parameters:
    interface_name (str): The name of the network interface for which to display statistics.

    Outputs:
    - Prints the status of the network interface (up or down).
    - Indicates if the interface is a VPN.
    - Prints the speed of the interface in Mbps.
    - Prints the duplex mode (full or half duplex).
    - Prints the MTU size in bytes.

    Example:
    >>> show_status('eth0')
    Status:       Up
    Is VPN:       No
    Speed:        1000 Mbps
    Duplex:       Full
    MTU:          1500 bytes

    Notes:
    - This function assumes that the `is_vpn` function is defined elsewhere in the code to determine if an interface is a VPN.
    - Requires the `psutil` library, which should be installed in the environment where this function is executed.

    """

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
    """
    Display I/O statistics for a specified network interface.

    This function retrieves and prints various input/output (I/O) statistics for a specified network interface
    using the psutil library. These statistics include data about bytes sent and received, packets transmitted and received,
    errors encountered, and packet drops.

    Parameters:
    interface_name (str): The name of the network interface for which to display I/O statistics.

    Outputs:
    - Prints the number of bytes sent and received.
    - Prints the number of packets sent and received.
    - Prints the number of errors encountered on the interface.
    - Prints the number of packets dropped on the interface.

    Example:
    >>> show_io_counters('eth0')
    Bytes Sent:      1234567890
    Bytes Received:  9876543210
    Packets Sent:    12345
    Packets Recv:    54321
    Errors In:       0
    Errors Out:      1
    Drop In:         0
    Drop Out:        0

    """

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
    """
    Display detailed information about all network interfaces on the system.

    This function retrieves and displays comprehensive details about each network interface on the system. It includes
    status, I/O statistics, and addresses for each interface. The function relies on the psutil library for retrieving
    network interface information and other system details.

    Steps Performed:
    1. Prints a header to indicate the start of the interfaces enumeration.
    2. Retrieves network interfaces and their addresses using psutil.net_if_addrs().
    3. Checks for internet access using the check_internet_access function.
    4. Iterates over each network interface, printing:
       - Interface name.
       - Status of the interface.
       - I/O statistics for the interface.
       - Address information for the interface.

    Note:
    - This function assumes the presence of additional functions: show_status, show_io_counters, and show_addresses, which
      provide details about the interface status, I/O counters, and address information, respectively.
    - Requires the psutil library, which should be installed in the environment where this function is executed.

    Example:
    >>> show()
    ===== INTERFACES ENUMERATION =====

    Interface: eth0
        Status:       Up
        Is VPN:       No
        Speed:        1000 Mbps
        Duplex:       Full
        MTU:          1500 bytes
        Bytes Sent:   1234567890
        Bytes Received: 9876543210
        Packets Sent: 12345
        Packets Recv: 54321
        Errors In:    0
        Errors Out:   1
        Drop In:      0
        Drop Out:     0
        IPv4 Address: 192.168.1.1
        Netmask:      255.255.255.0
        Broadcast:    192.168.1.255
        IPv6 Address: fe80::1
        Netmask:      64
        Broadcast:    ::

    """

    print("===== INTERFACES ENUMERATION =====\n")
    
    interfaces = psutil.net_if_addrs()
    
    check_internet_access()
    
    for interface_name, addresses in interfaces.items():
        print(f"\nInterface: {interface_name}")
        
        show_status(interface_name)
        show_io_counters(interface_name)
        show_addresses(addresses)
        
    print()