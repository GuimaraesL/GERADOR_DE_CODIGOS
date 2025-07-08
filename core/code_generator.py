import pandas as pd

def codigo_valido(codigo: str) -> bool:
    return isinstance(codigo, str) and len(codigo) in [6, 7] and codigo[:3].isalpha() and codigo[3:].isdigit()

def proximo_codigo(sigla: str, df_base: pd.DataFrame, digitos: int = 4) -> str:
    df_base = df_base[df_base['Codigo'].apply(codigo_valido)]
    df_base = df_base[df_base['Codigo'].str.startswith(sigla)]
    df_base = df_base[df_base['Codigo'].str.len() == (3 + digitos)]

    if df_base.empty:
        return f"{sigla}{'1'.zfill(digitos)}"

    numeros = df_base['Codigo'].str.extract(fr'{sigla}(\d{{{digitos}}})')[0].dropna()
    if numeros.empty:
        return f"{sigla}{'1'.zfill(digitos)}"

    numeros = numeros.astype(int)
    usados = set(numeros)
    lacunas = set(range(1, numeros.max() + 2)) - usados
    proximo = min(lacunas) if lacunas else numeros.max() + 1

    return f"{sigla}{str(proximo).zfill(digitos)}"