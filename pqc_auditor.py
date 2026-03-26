import subprocess
import os
import sys

# --- Config ---
SSH_DIR = "/etc/ssh/"
VULN_ALGOS = ['ssh-rsa', 'ecdsa-sha2-nistp256']
SAFE_ALGOS = ['ssh-ed25519', 'sntrup761x25519-sha512@openssh.com']
# ---------------------

def check_ssh_key(key_path):
    try:
        # Check la cle avec ssh-keygen natif
        output = subprocess.check_output(
            ['ssh-keygen', '-l', '-f', key_path], 
            stderr=subprocess.STDOUT, 
            text=True
        )
        
        if any(algo in output for algo in VULN_ALGOS):
            return "[VULNERABLE] Shor algorithm can break this"
        elif any(algo in output for algo in SAFE_ALGOS):
            return "[SAFE] Post-Quantum ready"
        
        return "[UNKNOWN] Manual check required"
        
    except Exception as e:
        return f"[ERROR] Can't read key: {e}"

if __name__ == "__main__":
    print("[INFO] Starting Quantum-Readiness Audit...")
    
    if not os.path.exists(SSH_DIR):
        print(f"[ERROR] Directory {SSH_DIR} does not exist.")
        sys.exit(1)
        
    # Chope toutes les cles publiques du dossier
    pub_keys = [os.path.join(SSH_DIR, f) for f in os.listdir(SSH_DIR) if f.endswith(".pub")]
    
    if not pub_keys:
        print(f"[WARN] No .pub keys found in {SSH_DIR} (Try creating one for testing)")
        
    for key in pub_keys:
        status = check_ssh_key(key)
        print(f"{key} -> {status}")