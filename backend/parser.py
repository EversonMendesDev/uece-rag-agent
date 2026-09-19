import pdfplumber

def extrair_texto_pdf(caminho_pdf: str) -> str:
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            # Extrai o texto mantendo o layout visual (útil para provas em duas colunas)
            texto_pagina = pagina.extract_text(layout=True)
            if texto_pagina:
                texto_completo += texto_pagina + "\n"
    return texto_completo

if __name__ == "__main__":
    caminho = "../data/prova_uece.pdf"
    try:
        conteudo = extrair_texto_pdf(caminho)
        print("--- Amostra do Texto Extraído ---")
        print(conteudo[:1000])
    except FileNotFoundError:
        print(f"Arquivo não encontrado. Coloque o PDF em: {caminho}")
        