import os
from datetime import datetime

folder_path = "."  # Path to the folder where the ping result files are located
prefix = "ping_results_"  # Prefix of the ping result files
output_file = "ping_stat.txt"  # Name of the output file

ping_count_per_day = {}
success_count_per_day = {}
failure_count_per_day = {}

# Get a list of files in the folder that start with the specified prefix
ping_result_files = [file for file in os.listdir(folder_path) if file.startswith(prefix)]

# Process each ping result file
for file_name in ping_result_files:
    #print("filename:", file_name)
    with open(os.path.join(folder_path, file_name), 'r') as file:
        for line in file:
            if line.strip():
                try:
                    timestamp_str, result = line.strip().split(": ", 1)
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    date_str = timestamp.date().isoformat()

                    # Increment the ping count for the day
                    ping_count_per_day[date_str] = ping_count_per_day.get(date_str, 0) + 1

                    # Determine if the ping was successful or failed
                    if "bytes from" in result:
                        success_count_per_day[date_str] = success_count_per_day.get(date_str, 0) + 1
                    else:
                        failure_count_per_day[date_str] = failure_count_per_day.get(date_str, 0) + 1

                except ValueError:
                    print("Error parsing line: ", line)

# Save the results to the output file and display the result
with open(output_file, 'w') as file:
    line = f"date,ping_count,success_count,failure_count\n"
    file.write(line)
    # Display the results
    for date, ping_count in ping_count_per_day.items():
        success_count = success_count_per_day.get(date, 0)
        failure_count = failure_count_per_day.get(date, 0)
        # Write the results without the title on a single line
        line = f"{date},{ping_count},{success_count},{failure_count}\n"
        file.write(line)

        print("Date:", date)
        print("Total pings:", ping_count)
        print("Successful pings:", success_count)
        print("Failed pings:", failure_count)
        print()