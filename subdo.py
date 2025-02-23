import subprocess
import sys
import time

def grab_subdomains(domain, output_file="subdomains.txt"):
    try:
        print(f"[+] Mencari subdomain untuk: {domain}")
        result = subprocess.run(["assetfinder", "--subs-only", domain], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("[-] Error saat menjalankan assetfinder!")
            print(result.stderr)
            return
        
        subdomains = result.stdout.splitlines()
        
        if subdomains:
            with open(output_file, "a") as f:
                for subdomain in subdomains:
                    f.write(subdomain + "\n")
                    print(f"[+] Ditemukan: {subdomain}")
            print(f"[+] Subdomain untuk {domain} berhasil disimpan di {output_file}")
        else:
            print(f"[-] Tidak ada subdomain ditemukan untuk {domain}.")
    except Exception as e:
        print(f"[-] Terjadi kesalahan: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py list.txt")
        sys.exit(1)
    
    list_file = sys.argv[1]
    
    try:
        with open(list_file, "r") as f:
            domains = [line.strip() for line in f.readlines() if line.strip()]
        
        for domain in domains:
            print(f"\n[+] Memproses domain: {domain}")
            grab_subdomains(domain)
            time.sleep(1)  # Menambahkan delay untuk menghindari rate limit
    except FileNotFoundError:
        print(f"[-] File {list_file} tidak ditemukan.")
