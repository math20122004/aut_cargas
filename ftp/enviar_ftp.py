import os
import sys
from ftplib import FTP
import paramiko
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from etl.utils import get_output_path as ge

load_dotenv()

def enviar_arquivos():
    servidor = os.getenv('FTP_SERVIDOR')
    usuario = os.getenv('FTP_USUARIO')
    caminho_chave_privada = os.getenv('CAMINHO_CHAVE_PRIVADA')
    senha_chave = os.getenv('SENHA_CHAVE_PRIVADA')
    pasta_remota = os.getenv('PASTA_REMOTA')

    caminho_local = ge()

    if not os.path.isdir(caminho_local):
        print(f"[ERRO] Pasta local '{caminho_local}' não existe.")
        return

    try:
        key = paramiko.RSAKey.from_private_key_file(caminho_chave_privada, password=senha_chave)
        transport = paramiko.Transport((servidor, 22))
        transport.connect(username=usuario, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        print(f"[OK] Conectado ao SFTP: {servidor}")

        try:
            sftp.chdir(pasta_remota)
            print(f"[OK] Acessando pasta remota: {pasta_remota}")
        except IOError:
            print(f"[ERRO] Pasta remota '{pasta_remota}' não encontrada.")
            sftp.close()
            return

        arquivos_enviados = 0
        for arquivo in os.listdir(caminho_local):
            caminho_arquivo = os.path.join(caminho_local, arquivo)
            if os.path.isfile(caminho_arquivo):
                sftp.put(caminho_arquivo, arquivo)
                print(f"[OK] Enviado: {arquivo}")
                arquivos_enviados += 1

        sftp.close()
        transport.close()
        print(f"[FINALIZADO] {arquivos_enviados} arquivos enviados com sucesso.")

    except Exception as e:
        print(f"[ERRO] Falha na conexão ou envio: {e}")
