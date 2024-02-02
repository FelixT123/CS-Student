import subprocess
import datetime
import time

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

    while True:
        result = f"{get_current_date()} {get_current_time()}: {ping_ip_address(ip_address,packet_size)}\n"
        filename = "ping_results_" + get_current_date() + ".txt"
        save_result_to_file(result, filename)
        print(result, end='')  # Print the result to the terminal without \n
        time.sleep(1)

if __name__ == "__main__":
    main()
