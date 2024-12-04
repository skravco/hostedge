import os
import time
import smtplib
import argparse
from scapy.all import ARP, Ether, srp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from concurrent.futures import ThreadPoolExecutor

# Mapping of network ranges to proper names
NETWORKS = {
    "192.168.0.0/24": "Home Wi-Fi",
    "172.16.10.0/24": "Office Network",
    "10.0.0.0/24": "Test Lab",
}

# Mailtrap Email Configuration
email_config = {
    'from_email': 'your_email@example.com',
    'to_email': 'recipient_email@example.com',
    'smtp_server': 'sandbox.smtp.mailtrap.io',
    'smtp_port': 2525,
    'username': os.getenv('MAILTRAP_USERNAME'),
    'password': os.getenv('MAILTRAP_PASSWORD'),
}


class ARPScanner:
    def __init__(self, networks, interface, known_hosts_file):
        self.networks = networks
        self.interface = interface
        self.known_hosts_file = known_hosts_file
        self.known_hosts = self.load_known_hosts()

    def load_known_hosts(self):
        """Load known hosts from the file."""
        if os.path.exists(self.known_hosts_file):
            with open(self.known_hosts_file, "r") as file:
                return set(file.read().splitlines())
        return set()

    def save_new_host(self, host):
        """Save a new host to the known hosts file."""
        with open(self.known_hosts_file, "a") as file:
            file.write(f"{host}\n")
        self.known_hosts.add(host)

    def scan_network(self, network, network_name):
        """Perform an ARP scan on the specified network."""
        print(f"Performing an ARP scan against {network} ({network_name})...")
        try:
            arp_request = ARP(pdst=network)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether / arp_request
            result = srp(packet, iface=self.interface, timeout=2, verbose=0)[0]

            active_hosts = set()
            for _, received in result:
                active_hosts.add(received.psrc)

            new_hosts = active_hosts - self.known_hosts
            for host in new_hosts:
                print(f"Found a new host on {network_name}: {host}")
                self.save_new_host(host)
                self.send_email_notification(host, network_name)
        except Exception as e:
            print(f"Error scanning {network_name} ({network}): {e}")

    def send_email_notification(self, host, network_name):
        """Send an email notification for a newly discovered host."""
        try:
            message = MIMEMultipart()
            message["From"] = email_config['from_email']
            message["To"] = email_config['to_email']
            message["Subject"] = f"New Host Detected on {network_name}"

            body = f"A new host was found on {network_name}:\n\nHost IP: {host}"
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.login(email_config['username'], email_config['password'])
                server.send_message(message)
                print(f"Notification sent for host: {host} on {network_name}")
        except Exception as e:
            print(f"Failed to send email notification: {e}")

    def monitor_networks(self):
        """Continuously monitor all networks for new hosts in parallel."""
        with ThreadPoolExecutor(max_workers=len(self.networks)) as executor:
            while True:
                futures = [
                    executor.submit(self.scan_network, network, network_name)
                    for network, network_name in self.networks.items()
                ]
                for future in futures:
                    future.result()  # Wait for all tasks to complete
                time.sleep(60)


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="ARP Scanner with email notifications.")
    parser.add_argument("--iface", required=True, help="Network interface to use for scanning.")
    parser.add_argument("--khf", default="hosts.txt", help="File to store known hosts (default: hosts.txt).")
    args = parser.parse_args()

    # Validate Mailtrap credentials
    if not email_config['username'] or not email_config['password']:
        print("Please set MAILTRAP_USERNAME and MAILTRAP_PASSWORD in your environment variables.")
        exit(1)

    # Initialize and run the ARP scanner
    scanner = ARPScanner(NETWORKS, args.iface, args.khf)
    try:
        scanner.monitor_networks()
    except KeyboardInterrupt:
        print("\nNetwork monitoring stopped.")
