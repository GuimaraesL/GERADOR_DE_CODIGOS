import pandas as pd
from typing import Dict, List, Set, Optional

# Mantém compatibilidade com as regras atuais: 3 letras + 3 ou 4 dígitos
def _codigo_valido_formato(codigo: str, digitos: int) -> bool:
    return (
        isinstance(codigo, str)
        and len(codigo) == 3 + digitos
        and codigo[:3].isalpha()
        and codigo[3:].isdigit()
    )

def _build_index(df_base: pd.DataFrame, digitos: int) -> Dict[str, Dict[str, object]]:
    """
    Cria um índice rápido por sigla -> { 'used': set[int], 'next': int }
    com base no DataFrame df_base['Codigo'].
    """
    index: Dict[str, Dict[str, object]] = {}
    if 'Codigo' not in df_base.columns:
        return index

    for code in df_base['Codigo']:
        if _codigo_valido_formato(code, digitos):
            sigla = code[:3]
            num = int(code[3:])
            entry = index.get(sigla)
            if entry is None:
                entry = {'used': set(), 'next': 1}
                index[sigla] = entry
            used: Set[int] = entry['used']  # type: ignore
            used.add(num)

    # Define o próximo faltante por sigla (menor número ausente ≥1)
    for entry in index.values():
        used: Set[int] = entry['used']  # type: ignore
        nxt = 1
        while nxt in used:
            nxt += 1
        entry['next'] = nxt

    return index

def gerar_codigos_em_lote(siglas: List[Optional[str]], df_base: pd.DataFrame, digitos: int = 4) -> List[Optional[str]]:
    """
    Gera códigos em lote mantendo a mesma lógica de preencher lacunas e
    atualizar a base incrementalmente por sigla.
    - siglas: lista possivelmente contendo None/NaN; retornamos None correspondente.
    - df_base: DataFrame com a coluna 'Codigo'. Não é modificado; o chamador decide se quer
      anexar os novos códigos ao seu df_base em memória (para consistência com a GUI atual).
    - digitos: 3 ou 4.
    Retorna lista do mesmo tamanho de 'siglas'.
    """
    idx = _build_index(df_base, digitos)
    out: List[Optional[str]] = []

    for sig in siglas:
        if sig is None or not isinstance(sig, str) or len(sig) < 3:
            out.append(None)
            continue

        sigla = sig[:3]
        entry = idx.get(sigla)
        if entry is None:
            entry = {'used': set(), 'next': 1}
            idx[sigla] = entry

        used: Set[int] = entry['used']  # type: ignore
        nxt: int = entry['next']        # type: ignore

        # Garante o menor faltante atual
        while nxt in used:
            nxt += 1

        code = f"{sigla}{str(nxt).zfill(digitos)}"
        out.append(code)

        # Atualiza estruturas para refletir a alocação
        used.add(nxt)
        nxt += 1
        while nxt in used:
            nxt += 1
        entry['next'] = nxt

    return out
