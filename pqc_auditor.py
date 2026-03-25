import subprocess
import os
from typing import Dict, List
from colorama import init, Fore, Style

init(autoreset=True)

# --- Configuration ---
# Chemin vers le dossier contenant les clés publiques à auditer
CHEMIN_DOSSIER_CLES = "/etc/ssh/"
VULNERABLE_ALGO = ['ssh-rsa', 'ecdsa-sha2-nistp256']
QUANTUM_SAFE_ALGO = ['ssh-ed25519', 'sntrup761x25519-sha512@openssh.com']
# ---------------------

def auditer_cle_publique(chemin_cle: str) -> Dict[str, str]:
    """Analyse mathématiquement une clé SSH pour vérifier sa résistance quantique."""
    try:
        resultat = subprocess.run(
            ['ssh-keygen', '-l', '-f', chemin_cle], 
            capture_output=True, text=True, check=True
        )
        sortie = resultat.stdout
        
        statut = "INCONNU"
        couleur = Fore.YELLOW
        
        if any(algo in sortie for algo in VULNERABLE_ALGO):
            statut = "VULNÉRABLE (Algorithme de Shor)"
            couleur = Fore.RED
        elif any(algo in sortie for algo in QUANTUM_SAFE_ALGO):
            statut = "SÉCURISÉ (Post-Quantum Safe)"
            couleur = Fore.GREEN
                
        return {"cle": chemin_cle, "statut": statut, "details": sortie.strip(), "couleur": couleur}
    except subprocess.CalledProcessError:
        return {"erreur": f"Impossible de lire ou parser {chemin_cle}"}

def lister_cles_publiques(dossier: str) -> List[str]:
    """Retourne la liste des fichiers .pub dans un dossier."""
    cles = []
    if os.path.exists(dossier):
        for fichier in os.listdir(dossier):
            if fichier.endswith(".pub"):
                cles.append(os.path.join(dossier, fichier))
    return cles

if __name__ == "__main__":
    print(f"{Style.BRIGHT}! Lancement de l'audit Post-Quantique de l'infrastructure...\n")
    
    cles_a_tester = lister_cles_publiques(CHEMIN_DOSSIER_CLES)
    
    if not cles_a_tester:
        print(f"! Aucune clé publique (.pub) trouvée dans {CHEMIN_DOSSIER_CLES}.")
        print("Pour tester, créez une fausse clé avec : ssh-keygen -t rsa -f /etc/ssh/test_rsa.pub")
    
    for cle in cles_a_tester:
        rapport = auditer_cle_publique(cle)
        if "erreur" in rapport:
            print(f"{Fore.RED}! Erreur sur {cle} : {rapport['erreur']}")
        else:
            print(f"! {Style.BRIGHT}{rapport['cle']}")
            print(f"   Détails : {rapport['details']}")
            print(f"   Statut  : {rapport['couleur']}{rapport['statut']}\n")