# Funções de limpeza e transformação
import pandas as pd
import re
import logging
import os

def clean_cell(cell: str) -> str:
    try:
        cell = str(cell)
        cell = re.sub(r'[;"“”\'’]', '', cell)     # Remove aspas e ponto e vírgula
        cell = re.sub(r'\s*\|\s*', '|', cell)     # Remove espaços ao redor do |
        cell = re.sub(r'\s+', ' ', cell)          # Substitui múltiplos espaços por 1
        return cell.strip()
    except Exception as e:
        logging.warning(f"Erro limpando célula: {cell} - {e}")
        return cell

def transform(df: pd.DataFrame, file_path: str = None) -> pd.DataFrame:
    logging.info("Iniciando transformação...")
    df = df.astype(str).applymap(clean_cell)

    CARGA_PDM = os.getenv("SQL_CG_PDM")

    # Remove uma linha extra se o caminho for um arquivo específico
    if file_path == CARGA_PDM:
        df = df.iloc[1:]  # remove a primeira linha
        logging.info("Linha extra removida devido ao arquivo carga de procedimentos.")

    logging.info("Transformação concluída. Forma final: %s", str(df.shape))
    return df
