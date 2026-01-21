# SentryScan - Advanced Python Port Scanner

A robust network analysis tool featuring both a CLI and a modern Web Interface. Capable of scanning IP addresses for open ports, detecting services, and visualizing results with interactive dashboards.

## Features
- **Dual Modes**: Command Line Interface (CLI) and Web Application (Flask).
- **Scanning**: Fast TCP connect scans with service version detection.
- **Visualization**: Interactive Donut and Bar charts for protocol and service distribution.
- **Reporting**: Export results to JSON or CSV.
- **Demo Mode**: Simulate scans to test the UI without external dependencies.
- **Smart Nmap Detection**: Automatically finds Nmap on Windows systems.

## Preview
![Dashboard](screenshots/hero.png)
*Modern Search Interface*

![Results](screenshots/dashboard.png)
*Interactive Results Dashboard*

## Project Statement
SentryScan is designed to bridge the gap between complex command-line network tools and modern user experience. By leveraging Nmap's powerful scanning engine and wrapping it in a sleek, responsive web interface, it makes network analysis accessible to both security professionals and enthusiasts.

## Prerequisites
- **Python 3.6+**
- **Nmap**: Required for actual scanning. [Download from nmap.org](https://nmap.org/download.html).

## Installation

1. Clone the repository.
   ```bash
   git clone https://github.com/arnabdevs/portscanner.git
   cd sentryscan
   ```
2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 🌐 Web Application (Recommended)
Launch the modern automation dashboard.
```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser.
- **Scan**: Enter an IP address.
- **Demo**: Click "Try Demo Mode" to preview the dashboard.

### 💻 CLI usage
Run the scanner from the terminal.
```bash
python ip_addr_scanner.py <target_ip> [options]
```
**Options:**
- `-o`, `--output <file>`: Save to JSON/CSV.
- `-v`, `--visualize`: Generate HTML report.
- `--demo`: Run in simulation mode.

## License
MIT License. See `LICENSE` file.

## Author
**Arnab Kumar Das**
