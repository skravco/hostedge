# HostEdge

 Python-based **network monitoring tool designed to scan multiple networks for newly connected devices** using ARP requests. It sends email notifications whenever a new host is discovered. It can monitor networks dynamically and efficiently in parallel.

## **Features**

- **Dynamic Network Scanning**: Monitors multiple networks and detects new devices connected to each network.
- **Email Notifications**: Sends email alerts for each new host discovered on the network.
- **Parallel Scanning**: Uses multi-threading for scanning multiple networks simultaneously, optimizing performance.
- **Customizable**: Configure the network interface and the file where known hosts are saved via command-line arguments.
- **Mailtrap Integration**: Send notifications through Mailtrap's SMTP server (you can replace with your own SMTP configuration).

## **Requirements**

- Python 3.6+ (Python 3.7 or higher recommended)
- `scapy` library for ARP scanning.
- Mailtrap account for email notifications (or your preferred SMTP server credentials).
  
### **Install Dependencies**

To run `HostEdge`, you'll need to install the required dependencies:

```bash
pip install scapy
```

Make sure to install any other dependencies as needed.

### **Setting Up Mailtrap**

You need an SMTP server to send email notifications. `HostEdge` uses Mailtrap for this purpose, but you can replace this with your own SMTP service by adjusting the `email_config` dictionary.

1. **Create a Mailtrap account**: Go to [Mailtrap](https://mailtrap.io/) and sign up for a free account.
2. **Get SMTP credentials**: After logging into Mailtrap, retrieve your SMTP credentials (`username`, `password`) and configure them in the environment variables:
   - `MAILTRAP_USERNAME`
   - `MAILTRAP_PASSWORD`

If you are using a different SMTP service, update the configuration in the `email_config` dictionary.

---

## **How to Use**

### **Command-Line Arguments**

To run `HostEdge`, the following command-line arguments are available:

- `--iface`: The network interface to scan (e.g., `eth0`, `wlan0`). This argument is **mandatory**.
- `--khf`: The file to store known hosts. If not provided, the default value is `hosts.txt`.

### **Basic Usage**

1. **Scan a network interface and track known hosts in the default file (`hosts.txt`)**:

```bash
python3 hostedge.py --iface eth0
```

2. **Scan a network interface and specify a custom file for known hosts**:

```bash
python3 hostedge.py --iface eth0 --khf my_hosts.txt
```

### **Explanation of Output**

- The script will scan the specified network interface (`eth0` in this case) for new hosts connected to predefined networks (`192.168.0.0/24`, `172.16.10.0/24`, `10.0.0.0/24`).
- Whenever a new host is found, it is added to the `hosts.txt` (or the file specified via `--khf`), and an email notification is sent to the provided email address.
- The script will continuously scan for new hosts every 60 seconds and notify you when a new host joins the network.

---

## **Code Walkthrough**

### **Main Components**

1. **`ARPScanner` Class**:
   - This class is responsible for scanning networks using ARP requests, detecting new hosts, saving known hosts, and sending email notifications.

2. **`scan_network` Method**:
   - Performs an ARP scan on the specified network, returning a set of active hosts.

3. **`send_email_notification` Method**:
   - Sends an email notification to the configured recipient using SMTP (configured for Mailtrap).

4. **`monitor_networks` Method**:
   - Continuously monitors all networks, performing ARP scans and checking for new hosts every 60 seconds.

### **Multi-Threading**

The script uses Python's `ThreadPoolExecutor` from the `concurrent.futures` module to scan multiple networks in parallel, optimizing performance when monitoring multiple networks.

---

## **Environment Variables for Mailtrap**

Before running the application, make sure to configure your Mailtrap SMTP credentials as environment variables:

- `MAILTRAP_USERNAME`: Your Mailtrap username.
- `MAILTRAP_PASSWORD`: Your Mailtrap password.

You can set these environment variables using the terminal:

```bash
export MAILTRAP_USERNAME="your_username"
export MAILTRAP_PASSWORD="your_password"
```

Alternatively, you can set them in your `.bashrc` or `.zshrc` file for persistent access.

---

## **Example Email Notification**

When a new host is discovered on one of your networks, you will receive an email with the following format:

---

**Subject**: `New Host Detected on Home Wi-Fi`

**Body**:
```
A new host was found on Home Wi-Fi:

Host IP: 192.168.0.5
```

---

## **Customization**

### **Network Configuration**

You can customize the list of networks that `HostEdge` monitors by editing the `NETWORKS` dictionary:

```python
NETWORKS = {
    "192.168.0.0/24": "Home Wi-Fi",
    "172.16.10.0/24": "Office Network",
    "10.0.0.0/24": "Test Lab",
}
```

Each entry in the dictionary represents a network range (CIDR) and a name to associate with it. You can add or modify entries as needed.

### **Interface Configuration**

The interface to use for ARP scanning is specified via the `--iface` argument. If you're using a wireless interface, use the appropriate interface name (e.g., `wlan0`).

---

## **Troubleshooting**

### **Common Errors**

1. **Permission Errors (ARP Scanning)**:
   - If you receive permission errors when performing the ARP scan, make sure the script is running with sufficient privileges (e.g., use `sudo` for network-related actions).

2. **SMTP Errors**:
   - Ensure your SMTP credentials are correct and that you have an active internet connection.
   - If you're using Mailtrap, check your SMTP settings and credentials in your Mailtrap account.

---

## **Contributions**

Contributions to `HostEdge` are welcome! If you find a bug or would like to add new features, feel free to fork the repository, make improvements, and submit a pull request.
