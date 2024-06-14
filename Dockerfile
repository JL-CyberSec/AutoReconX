# Use Official Kali linux image
FROM kalilinux/kali-rolling

# Update the system and install kali-linux-large package
RUN apt-get update
RUN apt-get install -y sudo
RUN sudo apt-get install --fix-missing
RUN sudo apt-get install -y --fix-missing python3-pip
RUN sudo apt-get install -y iptables
RUN sudo apt-get install -y nmap
RUN apt-get clean

RUN rm -rf /var/lib/apt/lists/*

# Stablish workdir
WORKDIR /home

# Copy the code in the /home path in the container
COPY . /home/AutoReconX

# Make the script executable
# RUN chmod +x /home/AutoReconX/install

# Run the script during the build process
# RUN /home/AutoReconX/install

# Command to keep the container up and in execution
CMD ["tail", "-f", "/dev/null"]
