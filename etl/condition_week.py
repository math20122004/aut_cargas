import datetime
import logging
import queue
import threading
import os
from dotenv import load_dotenv

def return_queys() -> list:
    try:
        load_dotenv()
        
        CARGA_USUARIO = os.getenv('SQL_CG_USUARIO')
        CARGA_LOT = os.getenv("SQL_CG_LOT")
        CARGA_LOT_3 = os.getenv("SQL_CG_LOT_3")
        CARGA_AUT = os.getenv("SQL_CG_AUT_1")
        CARGA_AUT_3 = os.getenv("SQL_CG_AUT_3")
        CARGA_AUT_90 = os.getenv("SQL_CG_AUT_90")
        CARGA_DAC = os.getenv("SQL_CG_DAC")
        CARGA_DAC_2 = os.getenv("SQL_CG_DAC_2")
        CARGA_CRD = os.getenv("SQL_CG_CRD")
        CARGA_PDM = os.getenv("SQL_CG_PDM")

        resp = None
        # Queue é uma função do py em que cria uma fila (FIFO) e é o mais seguro para trocar dados em threads, invés de usar var
        resposta_queue = queue.Queue()

        def perguntar_com_timeout(resposta_queue):
            try:
                resposta = input("Rodar carga procedimentos de 90 dias? [S/N]\n").strip()
                resposta_queue.put(resposta)
            except EOFError:
                resposta_queue.put(None)

        # Inicia a thread para perguntar ao usuário
        thread = threading.Thread(target=perguntar_com_timeout, args=(resposta_queue,))
        thread.start()

        # Espera até 30 segundos pela resposta
        thread.join(timeout=30)

        if thread.is_alive():
            logging.warning("Sem resposta do usuário dentro do tempo. Executando padrão.")
            resp = None
        else:
            resp = resposta_queue.get()
            logging.info(f"Resposta do usuário: {resp}")

        day_week = datetime.datetime.now().strftime('%A')
        day_number = datetime.datetime.now().day

        carga_week = []

        if day_week == "Monday":
            carga_week.extend([
                CARGA_LOT_3,
                CARGA_CRD,
                CARGA_USUARIO,
                CARGA_PDM
            ])

            if resp and resp.strip().upper() in ['S', 'SIM']:
                carga_week.append(CARGA_AUT_90)
            else:
                carga_week.append(CARGA_AUT_3)

            if day_number == 2:
                carga_week.append(CARGA_DAC)

            if day_number == 17:
                carga_week.append(CARGA_DAC)

        elif day_week in ["Tuesday", "Wednesday", "Thursday", "Friday"]:
            carga_week.extend([
                CARGA_LOT,
                CARGA_USUARIO
            ])

            if resp and resp.strip().upper() in ['S', 'SIM']:
                carga_week.append(CARGA_AUT_90)
            else:
                carga_week.append(CARGA_AUT)

            if day_number == 2:
                carga_week.append(CARGA_DAC_2)

            if day_number == 17:
                carga_week.append(CARGA_DAC)

        return carga_week

    except Exception as e:
        logging.exception(f"Erro em return_queys: {e}")
        return []
