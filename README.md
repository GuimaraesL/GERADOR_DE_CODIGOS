# GERADOR_DE_CODIGOS

Gerador de códigos sequenciais a partir de **siglas** (prefixos de 3 letras), com interface gráfica (Tkinter + ttkbootstrap) e integração com **Excel** (openpyxl/pandas). O app lê uma base de códigos existente, calcula o **próximo código disponível** para cada sigla (preenchendo lacunas) e grava o resultado de volta em uma nova aba do arquivo de entrada.

## ✨ Funcionalidades
- Importa uma **base de códigos** de um arquivo Excel.
- Extrai **siglas** (prefixos) de outro arquivo Excel.
- Gera o **próximo número disponível**, preenchendo lacunas.
- Alterna entre sufixo de **4** ou **3 dígitos**.
- Escreve o resultado em uma nova aba `RESULTADO` (sem sobrescrever).
- GUI simples com mensagens de sucesso/erro.

## 🚀 Como usar
1) Base de códigos (aba `aba1`, colunas A/B lidas a partir da linha 2).
2) Siglas (aba `SIGLAS`, coluna `A`).
3) Na GUI: **Selecionar base** → **Selecionar entrada** → (opcional) marcar **3 dígitos** → **Processar**.
   - Sai em `RESULTADO`, `RESULTADO1`, `RESULTADO2`, ...

## 🧮 Regras
- Formato aceito: `ABC0001` (4 dígitos) ou `ABC001` (3 dígitos).
- Considera apenas códigos válidos que **começam** com a sigla e têm comprimento `3 + N`.
- Seleciona o **menor número faltante**; se não houver, começa em `0001`/`001`.

## 📦 Requisitos
- Python 3.10+
- pandas, openpyxl, ttkbootstrap
