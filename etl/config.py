# CONFIG: Carrega variáveis de ambiente e configura logging.
import os
import logging
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Variáveis de ambiente
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_DSN = os.getenv("DB_DSN")
OUT_PATH = os.getenv("OUT_PATH", "./saida")  # Caminho padrão
CAMINHO_LOG = os.getenv("CAMINHO_LOG")
INSTANCE_CLIENTE = os.getenv("INSTANCE_CLIENT")

# Garante que a pasta exista
os.makedirs(OUT_PATH, exist_ok=True)
os.makedirs(CAMINHO_LOG, exist_ok=True)

# Configuração de log
logging.basicConfig(
    filename=os.path.join("logs", f"{CAMINHO_LOG}\\etl.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
