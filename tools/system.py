import subprocess

def show():
    print("===== SYSTEM INFORMATION =====\n")
    
    try:
        neofetch_output = subprocess.check_output(['neofetch'], text=True)
        print(neofetch_output)
    except subprocess.CalledProcessError as e:
        print(f"Error executing neofetch: {e}")
    except FileNotFoundError:
        print("neofetch is not installed. Please install it and try again.")
