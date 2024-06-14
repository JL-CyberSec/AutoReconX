import subprocess

def show():
    """
    Get firewall information of your machine
    """

    print("===== FIREWALL INFORMATION =====\n")
    
    try:
        iptables_output = subprocess.check_output(['sudo', 'iptables', '-L'], text=True)
        print("iptables rules:")
        print(iptables_output)
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")