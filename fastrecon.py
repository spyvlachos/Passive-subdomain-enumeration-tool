#!/usr/bin/env python3
import argparse  
import subprocess
import os

def run_command(cmd):
    print(f"[*] Running: {cmd}")
    try:
        # shell=True is needed for the pipes (|) and redirects (>>)
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Passive Recon Wrapper")
    parser.add_argument("-d", "--domains", help="Domains (comma-separated)", required=True)
    args = parser.parse_args()

    # Pull from the environment
    github_token = os.getenv("GITHUB_TOKEN")
    
    # Path to Desktop
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")

    domain_list = [d.strip() for d in args.domains.split(",")]

    for domain in domain_list:
        print(f"\n--- TARGET: {domain} ---")
        temp_file = os.path.join(desktop, f"{domain}_raw.txt")
        final_file = os.path.join(desktop, f"{domain}_alive.txt")

        # 1. Subfinder
        run_command(f"subfinder -d {domain} -silent >> {temp_file}")

        # 2. Amass (Using -o to save directly)
        run_command(f"amass enum -passive -d {domain} >> {temp_file}")

        # 3. CRT.SH
        run_command(f"curl -s 'https://crt.sh/?q=%25.{domain}&output=json' | jq -r '.[].name_value' | sed 's/\\*\\.//g' >> {temp_file}")
        
        # 4. GitHub (Only runs if token is found)
        if github_token:
            run_command(f"github-subdomains -d {domain} -t {github_token} >> {temp_file}")
        else:
            print("[!] Skipping GitHub: No GITHUB_TOKEN found in environment.")

        print(f"[*] Probing for alive hosts...")
        if os.path.exists(temp_file):
            # Using httpx-toolkit with shorthand flags for better compatibility
            run_command(f"cat {temp_file} | sort -u | httpx-toolkit -silent -sc -title -td -o {final_file}")
            
            
            print(f"[+] Success! Check your Desktop for {domain}_alive.txt")

if __name__ == "__main__":
    main()
