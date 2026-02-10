from flask import Flask, render_template, request, jsonify
import ip_addr_scanner as scanner_logic
import os

app = Flask(__name__)
# Alias for Vercel
app_instance = app

@app.route('/')
def index():
    return render_template('index.html')


def find_nmap():
    # Check system PATH first
    if os.system("where nmap >nul 2>&1") == 0:
        return None # Let python-nmap use default
    
    # Common Windows paths
    common_paths = [
        r"C:\Program Files (x86)\Nmap\nmap.exe",
        r"C:\Program Files\Nmap\nmap.exe"
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return [path] 
            
    return None

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    target = data.get('target')
    demo_mode = data.get('demo_mode', False)
    
    if not demo_mode and not target:
        return jsonify({'error': 'Target IP is required'}), 400

    try:
        if demo_mode:
            results = scanner_logic.generate_demo_data()
            target_host = "DEMO SCAN"
        else:
            if not scanner_logic.validate_target(target):
                return jsonify({'error': 'Invalid IP address or hostname'}), 400
            
            import nmap
            
            # Attempt to find nmap
            nmap_path_arg = find_nmap()
            print(f"DEBUG: Nmap path detected: {nmap_path_arg}")
            
            try:
                if nmap_path_arg:
                    nm = nmap.PortScanner(nmap_search_path=nmap_path_arg)
                else:
                    nm = nmap.PortScanner() # Hope it's in PATH
            except nmap.PortScannerError:
                 return jsonify({
                     'error': 'Nmap binary not found. This is common in serverless environments like Vercel.',
                     'code': 'NMAP_MISSING',
                     'suggestion': 'Use Demo Mode to preview the dashboard features.'
                 }), 500

            nm.scan(hosts=target, arguments='-v -sT -sV --version-light')
            
            results = []
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                     ports = nm[host][proto].keys()
                     for port in ports:
                         service = nm[host][proto][port]
                         results.append({
                             "host": host,
                             "hostname": nm[host].hostname(),
                             "protocol": proto,
                             "port": port,
                             "state": service.get('state'),
                             "service": service.get('name'),
                             "product": service.get('product', ''),
                             "version": service.get('version', '')
                         })
            target_host = target

        return jsonify({'results': results, 'target': target_host})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
