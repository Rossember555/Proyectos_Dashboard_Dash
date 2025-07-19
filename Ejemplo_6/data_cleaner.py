import re
import pandas as pd
from datetime import datetime

class DataCleaner:
    def __init__(self, df: pd.DataFrame, email_col: str, date_col: str, date_format: str):
        """
        df: DataFrame original
        email_col: nombre de la columna con emails
        date_col: nombre de la columna con fechas
        date_format: formato esperado de salida, p.ej. '%Y-%m-%d'
        """
        self.df = df.copy()
        self.email_col = email_col
        self.date_col = date_col
        self.date_format = date_format

    def clean_email(self):
        """Normaliza y corrige errores comunes en emails."""
        def _fix(email):
            if not isinstance(email, str):
                return None
            e = email.strip().lower()
            # reemplaza espacios y comas por punto
            e = re.sub(r'[\s,]+', '.', e)
            # corrige dominios mal escritos
            e = re.sub(r'@gamil\.com$', '@gmail.com', e)
            e = re.sub(r'@hotnail\.com$', '@hotmail.com', e)
            # valida sintaxis básica
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return e if re.match(pattern, e) else None

        self.df[self.email_col] = self.df[self.email_col].apply(_fix)
        return self

    def clean_date(self):
        """Convierte cadenas a datetime y formatea según self.date_format."""
        def _to_dt(val):
            for fmt in ('%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y'):
                try:
                    return datetime.strptime(val, fmt)
                except Exception:
                    continue
            return None

        # convertir y formatear
        self.df[self.date_col] = (
            self.df[self.date_col]
            .astype(str)
            .apply(_to_dt)
            .dropna()
            .apply(lambda d: d.strftime(self.date_format))
        )
        return self

    def get_clean_data(self) -> pd.DataFrame:
        """Devuelve el DataFrame limpio."""
        return self.df
