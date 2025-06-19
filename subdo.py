import subprocess
import sys
import time
import concurrent.futures
import threading

lock = threading.Lock()  # Supaya tidak bentrok saat menulis file

def grab_subdomains(domain, output_file="subdomains.txt", timeout=30):
    try:
        print(f"[+] Mencari subdomain untuk: {domain}")
        result = subprocess.run(
            ["assetfinder", "--subs-only", domain],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode != 0:
            print(f"[-] Error saat menjalankan assetfinder untuk {domain}!")
            print(result.stderr)
            return
        
        subdomains = result.stdout.splitlines()
        
        if subdomains:
            with lock:
                with open(output_file, "a", encoding='utf-8') as f:
                    for subdomain in subdomains:
                        f.write(subdomain + "\n")
                        print(f"[+] Ditemukan: {subdomain}")
            print(f"[+] Subdomain untuk {domain} berhasil disimpan di {output_file}")
        else:
            print(f"[-] Tidak ada subdomain ditemukan untuk {domain}.")
    except subprocess.TimeoutExpired:
        print(f"[-] Timeout: proses untuk {domain} melebihi {timeout} detik, dilewati.")
    except Exception as e:
        print(f"[-] Terjadi kesalahan pada {domain}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py list.txt")
        sys.exit(1)
    
    list_file = sys.argv[1]
    
    try:
        with open(list_file, "r", encoding='utf-8') as f:
            domains = [line.strip() for line in f.readlines() if line.strip()]
        
        print(f"[+] Total domain: {len(domains)}")

        # Pakai ThreadPoolExecutor (misal: 5 thread paralel)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_domain = {
                executor.submit(grab_subdomains, domain): domain for domain in domains
            }
            
            for future in concurrent.futures.as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"[-] Error pada domain {domain}: {e}")
    
    except FileNotFoundError:
        print(f"[-] File {list_file} tidak ditemukan.")
