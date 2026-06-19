import socket
import os
import sys

def scan_local_environment():
    config_file = "ports_config.txt"
    report_file = "Network_Report.md"
    
    print("🚀 [STARTING AUTOMATED LOCAL NETWORK AUDIT]")
    print("-" * 50)
    
    # Check if the target configuration layout exists
    if not os.path.exists(config_file):
        print(f"❌ FAILURE: Configuration asset tracking file '{config_file}' is missing!")
        sys.exit(1)
        
    print(f"🔍 Reading target scan criteria from {config_file}...")
    
    # Initialize our Markdown report table structure
    report_lines = [
        "# Local Infrastructure Network Audit Report\n",
        "| Port | Intended Service | Operational Status |",
        "| :--- | :--------------- | :----------------- |"
    ]
    
    # Process ports configuration matrix line by line
    with open(config_file, "r", encoding="utf-8") as file:
        for line in file:
            # Skip empty lines or commented-out configuration notes
            if not line.strip() or line.startswith("#"):
                continue
            
            try:
                port_str, service_name = line.strip().split(":")
                port = int(port_str)
            except ValueError:
                print(f"⚠️ Skipping malformed line layout: {line.strip()}")
                continue
            
            # Setup a low-level network socket probe connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0) # 1-second maximum wait window per validation trace
            
            # Execute loopback test trace on localhost interface
            result = sock.connect_ex(('127.0.0.1', port))
            
            if result == 0:
                print(f"✅ PORT {port:5} [OPEN]   -> {service_name} is actively running!")
                status = "🟢 ACTIVE / OPEN"
            else:
                print(f"⚠️ PORT {port:5} [CLOSED] -> {service_name} is idle/offline.")
                status = "🔴 OFFLINE / CLOSED"
                
            report_lines.append(f"| {port} | {service_name} | {status} |")
            sock.close()
            
    print("-" * 50)
    print(f"💾 Writing system audit configuration maps to local filesystem...")
    
    # 🛠️ THE CRITICAL WINDOWS ENCODING PATCH:
    # Explicitly declaration of encoding='utf-8' bypasses default fallback to 'cp1252' / 'charmap'
    with open(report_file, "w", encoding="utf-8") as rep:
        rep.write("\n".join(report_lines))
        
    print(f"🎉 SUCCESS: Automated scan complete. Local markdown file generated: '{report_file}'")

if __name__ == "__main__":
    scan_local_environment()