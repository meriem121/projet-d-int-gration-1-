import paramiko
import time
from datetime import datetime

# Informations de connexion
hostname = "192.168.43.112"  
port = 22             
username = "chaima"     
password = "chaima2003"  

# Fonction pour surveiller les processus
def surveiller_processus(ssh):
    stdin, stdout, stderr = ssh.exec_command('top -bn1 | head -n 5')
    print("\n=== Surveillance des processus ===")
    print(stdout.read().decode())

# Fonction pour surveiller l'espace disque
def surveiller_espace_disque(ssh):
    stdin, stdout, stderr = ssh.exec_command('df -h')
    print("\n=== Surveillance de l'espace disque ===")
    print(stdout.read().decode())

# Fonction pour exécuter des commandes d'administration
def executer_commande_admin(ssh):
    while True:
        print("\nOptions d'administration:")
        print("1. Redémarrer le serveur")
        print("2. Arrêter le serveur")
        print("3. Voir les logs système")
        print("4. Quitter")
        
        choix = input("Choisissez une option (1-4): ")
        
        if choix == '1':
            ssh.exec_command('sudo reboot')
            print("Commande de redémarrage envoyée.")
            return
        elif choix == '2':
            ssh.exec_command('sudo shutdown -h now')
            print("Commande d'arrêt envoyée.")
            return
        elif choix == '3':
            stdin, stdout, stderr = ssh.exec_command('tail -n 20 /var/log/syslog')
            print(stdout.read().decode())
        elif choix == '4':
            return
        else:
            print("Option invalide.")

# Fonction principale
def main():
    # Créer une instance SSHClient
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Se connecter à la machine virtuelle
        ssh.connect(hostname, port=port, username=username, password=password)
        print(f"\n{datetime.now()} - Connexion SSH établie avec succès")

        while True:
            print("\nMenu Principal:")
            print("1. Surveillance système")
            print("2. Administration")
            print("3. Quitter")
            
            choix = input("Choisissez une option (1-3): ")
            
            if choix == '1':
                surveiller_processus(ssh)
                surveiller_espace_disque(ssh)
            elif choix == '2':
                executer_commande_admin(ssh)
            elif choix == '3':
                break
            else:
                print("Option invalide.")

    except paramiko.AuthenticationException:
        print("Échec de l'authentification. Vérifiez vos identifiants.")
    except paramiko.SSHException as e:
        print(f"Erreur SSH : {e}")
    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        # Fermer la connexion SSH
        ssh.close()
        print(f"{datetime.now()} - Connexion SSH fermée")

if __name__ == "__main__":
    main()
