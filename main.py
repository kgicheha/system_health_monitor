import psutil # (retrieves running processes and sysyem utilization)
import time
import csv
from datetime import datetime

def bytes_to_mb(bytes_val):
    #coverts bytes to megabytes
    return round(bytes_val / (1024 * 1024), 2)

def monitor(interval = 5, csv_filename="system_health_log.csv"):
    fieldnames = ['timestamp', 'cpu_percent', 'memory_percent', 'disk_percent',
                  'net_sent_MB', 'net_recv_MB', 'cpu_alert']


    # Setup CSV file
    with open(csv_filename, mode ='w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        csv_writer.writeheader()

        net_io_prev = psutil.net_io_counters()

        while True:

            # Timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # CPU, memory, disk
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            # Network I/O
            # # provides system-wide network input/output statistics.
            # It returns these statistics as a named tuple (or a dictionary

            net_io_curr = psutil.net_io_counters()

            net_io_prev = net_io_curr

            net_sent = bytes_to_mb(net_io_curr.bytes_sent - net_io_prev.bytes_sent)
            net_recv = bytes_to_mb(net_io_curr.bytes_recv - net_io_prev.bytes_recv)



            # CPU alert if CPU usage is over 50 %
            cpu_alert = "High CPU Usage!" if cpu > 50 else ""

            # Write to CSV
            csv_writer.writerow({
                'timestamp': timestamp,
                'cpu_percent': cpu,
                'memory_percent': memory,
                'disk_percent': disk,
                'net_sent_MB': net_sent,
                'net_recv_MB': net_recv,
                'cpu_alert': cpu_alert
            })
            # net_io_prev = net_io_curr

            time.sleep(interval)

if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\nMonitoring stopped. Data saved to 'system_health_log.csv'")
