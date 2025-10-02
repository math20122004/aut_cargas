# Lógica de extração do banco de dados
import pandas as pd
import oracledb
import logging
from .config import DB_USER, DB_PASS, DB_DSN, INSTANCE_CLIENTE

# Inicializa Oracle Client
oracledb.init_oracle_client(lib_dir=INSTANCE_CLIENTE)

def extract(query: str) -> pd.DataFrame:
    logging.info("Conectando ao Oracle...")
    with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN) as conn:
        logging.info("Executando query...")
        df = pd.read_sql(query, con=conn)
    logging.info("Extração concluída. Linhas: %d", len(df))
    return df
