import pdfplumber

def extrair_texto_pdf(caminho_pdf: str) -> str:
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        # Pula as duas primeiras páginas e processa o restante
        for pagina in pdf.pages[2:]:
            largura = pagina.width
            altura = pagina.height
            meio = largura / 2
            
            # Corta a página ao meio em duas colunas
            coluna_esquerda = pagina.crop((0, 0, meio, altura)).extract_text() or ""
            coluna_direita = pagina.crop((meio, 0, largura, altura)).extract_text() or ""
            
            # Junta primeiro o texto da esquerda, depois o da direita
            texto_completo += coluna_esquerda + "\n" + coluna_direita + "\n"
            
    return texto_completo

if __name__ == "__main__":
    caminho = "../data/prova_uece.pdf"
    try:
        conteudo = extrair_texto_pdf(caminho)
        print("--- Amostra do Texto Extraído em 2 Colunas ---")
        print(conteudo[:1000])
    except FileNotFoundError:
        print(f"Arquivo não encontrado em: {caminho}")