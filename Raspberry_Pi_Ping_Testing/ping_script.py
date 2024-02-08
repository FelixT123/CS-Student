import subprocess
import datetime
import time
import os
import curses
import sys
import socket

def get_ip_address():
    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Connect to a remote host (doesn't matter which one)
        sock.connect(("8.8.8.8", 80))
        
        # Get the local IP address from the connected socket
        ip_address = sock.getsockname()[0]
    except socket.error:
        # If an error occurs, return None or handle the exception
        ip_address = None
    finally:
        # Close the socket
        sock.close()
    return ip_address

def clear_screen():
    if os.name == 'posix':  # for Linux/OS X
        _ = os.system('clear')
    else:  # for Windows
        _ = os.system('cls')

def read_configuration(filename):
    config = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            config[key.strip()] = value.strip()
    return config

def ping_ip_address(ip_address, packet_size):
    if packet_size > 68:
        packet_size = 68
    try:
        ping_output = subprocess.check_output(["ping", "-c", "1", "-s", str(packet_size), "-W", "1", ip_address], universal_newlines=True)
        # ping one packet, timout 1 sec, packet size 68 bytes (max allowed is 68)
        # Parse the output to extract the relevant information
        lines = ping_output.split('\n')
        for line in lines:
            if 'bytes from' in line:
                filtered_line = line.replace(': icmp_seq=1', '').replace('ttl', 'TTL')
                return filtered_line
    except subprocess.CalledProcessError as e:
        filtered_line = f"Ping {ip_address} failed"
        return filtered_line

def save_result_to_file(result, filename):
    with open(filename, "a") as file:
        file.write(result)

def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def main():
    config = read_configuration('ping.conf')
    ip_address = config.get('ip_address') 
    packet_size = int(config.get('packet_size'))  # packet size in bytes and 68 is the max value allowed. Value larger than 68 will cause ping loss

    # Create a list to store the lines
    lines = []

    while True:
        result = f"{get_current_date()} {get_current_time()}: {ping_ip_address(ip_address,packet_size)}\n"
        filename = "ping_results_" + get_current_date() + ".txt"
        save_result_to_file(result, filename)
        
        split_line = result.rsplit(":", 1)
        if len(split_line) == 2:
            timestamp = split_line[0]
            ttl_and_time = split_line[1]
            # Remove the newline character
            ttl_and_time = ttl_and_time.replace("\n", "")
            #print(timestamp)
            #print(ttl_and_time, end='')

            # Add the latest line to the list
            lines.append(timestamp)
            if len(lines) > 14:
                lines.pop(0)
            lines.append(ttl_and_time)
            if len(lines) > 14:
                lines.pop(0)

        else:
            #print(result, end='')  # Print the result to the terminal without \n
            lines.append(result)
            # If the number of lines exceeds 14, remove the oldest line
            if len(lines) > 14:
                lines.pop(0)

        # Clear the terminal
        clear_screen()# Clear the terminal

        # Call the function to get the IP address
        ip = get_ip_address()
        print("My IP address:", ip)

        # Display the last 14lines
        for line in lines[-14:]:
            print(line)

        time.sleep(1)

if __name__ == "__main__":
    main()