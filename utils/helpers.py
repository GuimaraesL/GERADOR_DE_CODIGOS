import string

def letra_para_coluna(letra: str) -> int:
    letra = letra.upper()
    valor = 0
    for i, char in enumerate(reversed(letra)):
        valor += (string.ascii_uppercase.index(char) + 1) * (26 ** i)
    return valor