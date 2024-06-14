import sys
import termios
import tty
import tools.intro as intro
import tools.interfaces as interfaces
import tools.devices as devices

def ask_for_next_step():
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
    interfaces,
    devices
]

if __name__ == "__main__":
    for service in services:
        service.show()
        ask_for_next_step()