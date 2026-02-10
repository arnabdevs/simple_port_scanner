import nmap
import argparse
import sys
import socket
import csv
import json
import os
import random
import os
import random
from datetime import datetime

def validate_target(target):
    """validates if the target is a valid IP or hostname."""
    try:
        socket.gethostbyname(target)
        return True
    except socket.error:
        return False

def save_results_json(results, filepath):
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4)
        print(f"Results saved to {filepath}")

def save_results_csv(results, filepath):
    if not results:
        return
    keys = results[0].keys()
    with open(filepath, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
        print(f"Results saved to {filepath}")

def generate_demo_data():
    services = ['http', 'https', 'ssh', 'ftp', 'smtp', 'dns', 'mysql', 'rdp']
    products = ['nginx', 'Apache', 'OpenSSH', 'vsftpd', 'Postfix', 'dnsmasq', 'MySQL', 'Microsoft RDP']
    data = []
    print("Generating demo data...")
    for _ in range(20):
        idx = random.randint(0, len(services)-1)
        data.append({
            "host": f"192.168.1.{random.randint(1, 254)}",
            "hostname": f"demo-host-{random.randint(1, 100)}",
            "protocol": "tcp",
            "port": random.randint(20, 9000),
            "state": "open",
            "service": services[idx],
            "product": products[idx],
            "version": f"{random.randint(1,9)}.{random.randint(0,9)}"
        })
    return data

def scan_host(target, ports, output_file=None, visualize=False, demo_mode=False):
    scan_data = []

    if demo_mode:
        scan_data = generate_demo_data()
    else:
        scanner = nmap.PortScanner()
        print(f"Starting scan on {target} ports: {ports}...")
        try:
            scanner.scan(hosts=target, ports=ports, arguments='-v -sT -sV --version-light')
        except nmap.PortScannerError as e:
            print(f"Nmap error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

        for host in scanner.all_hosts():
            print(f"Host: {host} ({scanner[host].hostname()})")
            for proto in scanner[host].all_protocols():
                ports_list = scanner[host][proto].keys()
                for port in sorted(ports_list):
                    service = scanner[host][proto][port]
                    service_info = {
                        "host": host,
                        "hostname": scanner[host].hostname(),
                        "protocol": proto,
                        "port": port,
                        "state": service.get('state'),
                        "service": service.get('name'),
                        "product": service.get('product', ''),
                        "version": service.get('version', '')
                    }
                    scan_data.append(service_info)

    # Output Handling
    if output_file:
        if output_file.endswith('.json'):
            save_results_json(scan_data, output_file)
        elif output_file.endswith('.csv'):
            save_results_csv(scan_data, output_file)
        else:
            print("Unsupported file format for output. Please use .json or .csv")

    if visualize:
        report_file = "scan_report.html"
        if output_file:
             base_name = os.path.splitext(output_file)[0]
             report_file = f"{base_name}_report.html"
        generate_report(scan_data, report_file)

def main():
    parser = argparse.ArgumentParser(description="Python Nmap Port Scanner")
    parser.add_argument("target", nargs='?', help="Target IP address or hostname to scan")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range to scan (default: 1-1024)")
    parser.add_argument("-o", "--output", help="Output file path (supports .json, .csv)")
    parser.add_argument("-v", "--visualize", action="store_true", help="Generate HTML visualization report")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode with dummy data (no nmap required)")

    args = parser.parse_args()

    if args.demo:
        scan_host("DEMO", args.ports, args.output, args.visualize, demo_mode=True)
    elif args.target:
        if not validate_target(args.target):
            print(f"Error: Invalid target '{args.target}'. Please provide a valid IP or hostname.")
            sys.exit(1)
        scan_host(args.target, args.ports, args.output, args.visualize, demo_mode=False)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
