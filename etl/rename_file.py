from datetime import date
import os


def rename_file(file) -> str:
    today = date.today().strftime("%Y%m%d")

    if file == os.getenv("SQL_CG_USUARIO"):
        return f"USU_{today}.txt"
    elif file == os.getenv("SQL_CG_LOT"):
        return f"LOT_{today}.txt"
    elif file == os.getenv("SQL_CG_LOT_3"):
        return f"LOT_{today}.txt"
    elif file == os.getenv("SQL_CG_AUT_1"):
        return f"AUT_{today}.txt"
    elif file == os.getenv("SQL_CG_AUT_3"):
        return f"AUT_{today}.txt"
    elif file == os.getenv("SQL_CG_AUT_90"):
        return f"AUT_{today}.txt"
    elif file == os.getenv("SQL_CG_CRD"):
        return f"CRD_{today}.txt"
    elif file == os.getenv("SQL_CG_PDM"):
        return f"PDM_{today}.txt"
    elif file == os.getenv("SQL_CG_DAC"):
        return f"DAC_{today}.txt"
    elif file == os.getenv("SQL_CG_DAC_2"):
        return f"DAC_{today}.txt"
    