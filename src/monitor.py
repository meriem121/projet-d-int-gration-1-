import paramiko
import time

class SystemMonitor:
    def __init__(self, host, username, password=None, key_path=None):
        self.host = host
        self.username = username
        self.password = password
        self.key_path = key_path
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """Établit une connexion SSH"""
        try:
            if self.password:
                self.ssh.connect(self.host, username=self.username, password=self.password)
            elif self.key_path:
                self.ssh.connect(self.host, username=self.username, key_filename=self.key_path)
            print(f"✅ Connecté à {self.host}")
            return True
        except Exception as e:
            print(f"❌ Échec de la connexion : {e}")
            return False

    def get_cpu_usage(self):
        """Récupère l'utilisation du CPU"""
        stdin, stdout, stderr = self.ssh.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'")
        return float(stdout.read().decode().strip())

    def get_memory_usage(self):
        """Récupère l'utilisation de la mémoire"""
        stdin, stdout, stderr = self.ssh.exec_command("free -m | grep Mem | awk '{print $3/$2 * 100}'")
        return float(stdout.read().decode().strip())

    def get_disk_usage(self):
        """Récupère l'utilisation du disque"""
        stdin, stdout, stderr = self.ssh.exec_command("df -h / | tail -1 | awk '{print $5}' | tr -d '%'")
        return float(stdout.read().decode().strip())

    def manage_service(self, service, action):
        """Gère un service (start/stop/restart/status)"""
        stdin, stdout, stderr = self.ssh.exec_command(f"sudo systemctl {action} {service}")
        return stdout.read().decode().strip()

    def close(self):
        """Ferme la connexion SSH"""
        self.ssh.close()
        print("🔌 Connexion SSH fermée")

# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration (à adapter)
    config = {
        "host": "192.168.1.100",
        "username": "admin",
        "password": "votre_mot_de_passe"  # Optionnel : "key_path": "~/.ssh/id_rsa"
    }

    monitor = SystemMonitor(**config)
    
    if monitor.connect():
        try:
            print(f"  CPU: {monitor.get_cpu_usage()}%")
            print(f" RAM: {monitor.get_memory_usage()}%")
            print(f" Disque: {monitor.get_disk_usage()}%")
            
            # Exemple : vérification du service SSH
            print(f"🔧 Service SSH: {monitor.manage_service('ssh', 'status')}")
        finally:
            monitor.close()
