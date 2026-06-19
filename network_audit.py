import socket
import os
import sys

def scan_local_environment():
    config_file = "ports_config.txt"
    report_file = "Network_Report.md"
    
    print("🚀 [STARTING AUTOMATED LOCAL NETWORK AUDIT]")
    print("-" * 50)
    
    if not os.path.exists(config_file):
        print(f"❌ FAILURE: Configuration asset tracking file '{config_file}' is missing!")
        sys.exit(1)
        
    print(f"🔍 Reading target scan criteria from {config_file}...")
    
    report_lines = [
        "# Local Infrastructure Network Audit Report\n",
        "| Port | Intended Service | Operational Status |",
        "| :--- | :--------------- | :----------------- |"
    ]
    
    with open(config_file, "r") as file:
        for line in file:
            if not line.strip() or line.startswith("#"):
                continue
            
            port_str, service_name = line.strip().split(":")
            port = int(port_str)
            
            # Create a socket connection test probe
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0) # Wait maximum 1 second per probe
            
            # Attempt to connect to localhost on the targeted port
            result = sock.connect_ex(('127.0.0.1', port))
            
            if result == 0:
                print(f"✅ PORT {port:5} [OPEN]   -> {service_name} is actively running!")
                status = "🟢 ACTIVE / OPEN"
            else:
                print(f"⚠️ PORT {port:5} [CLOSED] -> {service_name} is idle/offline.")
                status = "🔴 OFFLINE / CLOSED"
                
            report_lines.append(f"| {port} | {service_name} | {status} |")
            sock.close()
            
    # Automatically output a markdown report summary asset
    with open(report_file, "w") as rep:
        rep.write("\n".join(report_lines))
        
    print("-" * 50)
    print(f"🎉 SUCCESS: Automated scan complete. Local markdown file generated: '{report_file}'")

if __name__ == "__main__":
    scan_local_environment()