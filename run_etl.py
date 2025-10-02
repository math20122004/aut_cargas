from datetime import datetime
import os
import logging

from etl.extract import extract
from etl.transform import transform as tr
from etl.load import load_txt
from etl.utils import read_query, get_output_path
import etl.condition_week as cw
import etl.rename_file as rf
from ftp.enviar_ftp import enviar_arquivos


def main():
    try:
        start = datetime.now()
         
        sql_files = cw.return_queys()

        print(f"\nCargas rodadas: {sql_files}")

        for sql_file in sql_files:
            logging.info(f"Processando arquivo {sql_file}...")

            file_name = rf.rename_file(sql_file)
            out_path = os.path.join(get_output_path(), file_name)
            query = read_query(sql_file)
            df = extract(query)
            df2 = tr(df, sql_file)
            load_txt(df2, out_path)

        enviar_arquivos()
        elapsed = (datetime.now() - start).total_seconds()
        logging.info("ETL finalizado com sucesso em %.1f seg", elapsed)

    except Exception as e:
        logging.exception("Erro no ETL: %s", str(e))
        raise

if __name__ == "__main__":
    main()
