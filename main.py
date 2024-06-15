import sys
import termios
import tty
import tools.intro as intro
import tools.system as system
import tools.interfaces as interfaces
import tools.firewall as firewall
import tools.hosts as hosts
import tools.goodbye as goodbye

def ask_for_next_step():
    """
    Prompt the user to press any key to continue or cancel with Esc.

    This function prints a message asking the user to press any key to continue
    or press the Esc key to cancel the operation. It sets the terminal to
    cbreak mode to read single keypresses without waiting for a newline. If the
    Esc key is pressed, the function prints "Cancelled" and exits the program.
    Otherwise, it prints a newline and returns control to the caller.

    Note:
        This function is designed for use in Unix-like operating systems.
        It may not work as intended on Windows.

    Raises:
        SystemExit: If the user presses the Esc key, the program will exit.
    """

    print("Press any key to continue or cancel with Esc")
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setcbreak(fd)
        
        while True:
            key = sys.stdin.read(1)
            if key == '\x1b':
                print("Cancelled")
                exit()
            else:
                print()
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

services = [
    intro,
    system,
    interfaces,
    firewall,
    hosts,
    goodbye
]

if __name__ == "__main__":
    for service in services:
        service.show()
        ask_for_next_step()