import os
import sys
from ftplib import FTP
import paramiko
from dotenv import load_dotenv
from etl.utils import get_output_path as ge

# Adiciona o diretório pai ao sys.path para importar utilitários
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()

def enviar_arquivos():
    servidor = os.getenv('FTP_SERVIDOR')
    usuario = os.getenv('FTP_USUARIO')
    caminho_chave_privada = os.getenv('CAMINHO_CHAVE_PRIVADA')
    senha_chave = os.getenv('SENHA_CHAVE_PRIVADA')
    pasta_remota = os.getenv('PASTA_REMOTA')
    pasta_remota_dac = os.getenv('PASTA_REMOTA_DAC')

    caminho_local = ge()

    if not os.path.isdir(caminho_local):
        print(f"[ERRO] Pasta local '{caminho_local}' não existe.")
        return

    try:
        # Conecta via SFTP
        key = paramiko.RSAKey.from_private_key_file(caminho_chave_privada, password=senha_chave)
        transport = paramiko.Transport((servidor, 22))
        transport.connect(username=usuario, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        print(f"[OK] Conectado ao SFTP: {servidor}")

        arquivos_enviados = 0

        for arquivo in os.listdir(caminho_local):
            caminho_arquivo = os.path.join(caminho_local, arquivo)

            if not os.path.isfile(caminho_arquivo):
                continue  # Pula se não for arquivo

            # Define a pasta remota com base no nome do arquivo
            if arquivo.startswith('DAC'):
                pasta_destino = pasta_remota_dac
            else:
                pasta_destino = pasta_remota

            try:
                sftp.chdir(pasta_destino)
            except IOError:
                print(f"[ERRO] Pasta remota '{pasta_destino}' não encontrada.")
                continue

            # Envia o arquivo
            sftp.put(caminho_arquivo, arquivo)
            arquivos_enviados += 1
            print(f"[OK] Enviado: {arquivo} → {pasta_destino}")

        sftp.close()
        transport.close()
        print(f"[FINALIZADO] {arquivos_enviados} arquivos enviados com sucesso.")

    except Exception as e:
        print(f"[ERRO] Falha na conexão ou envio: {e}")
