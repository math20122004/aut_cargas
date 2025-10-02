import os
from datetime import datetime
from etl.config import OUT_PATH

# Funções auxiliares (ex: read_query)
def read_query(file_path: str) -> str:
    with open(file_path, "r", encoding="latin-1") as f:
        return f.read()


MESES_PT = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
]

def get_output_path():
    hoje = datetime.now()
    nome_mes = MESES_PT[hoje.month - 1].upper()
    dia = hoje.day

    mes_path = os.path.join(OUT_PATH, nome_mes)
    os.makedirs(mes_path, exist_ok=True)

    dia_path = os.path.join(mes_path, str(dia))
    os.makedirs(dia_path, exist_ok=True)

    return dia_path