# Função que salva o arquivo final
import pandas as pd
import logging

def load_txt(df: pd.DataFrame, out_path: str):
    logging.info(f"Gravando arquivo TXT em {out_path}...")
    linhas = df.apply(lambda row: ''.join(row.values), axis=1)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write('\n'.join(linhas))
    logging.info("Arquivo gravado com sucesso.")
