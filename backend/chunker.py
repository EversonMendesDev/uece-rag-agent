import re
from parser import extrair_texto_pdf

def separar_questoes(texto: str) -> list[dict]:
    # Captura marcadores no formato "01.", "02." seguidos do início de texto da questão
    padrao_questao = r'(?:^|\n)\s*(\d{2}\.\s+[A-ZÀ-Ú0-9])'
    
    # Split preservando a separação exata
    partes = re.split(r'(?:^|\n)\s*(\d{2}\.)', texto)
    
    questoes = []
    for i in range(1, len(partes), 2):
        num_questao = partes[i].strip()
        corpo = partes[i+1].strip() if i+1 < len(partes) else ""
        
        # Filtra falsos positivos (ex: linhas de numeração do texto de apoio que não são questões)
        if len(corpo) > 20:
            questoes.append({
                "titulo": f"Questão {num_questao}",
                "conteudo": f"{num_questao} {corpo}"
            })
    return questoes

if __name__ == "__main__":
    caminho_pdf = "../data/prova_uece.pdf"
    try:
        texto_bruto = extrair_texto_pdf(caminho_pdf)
        questoes = separar_questoes(texto_bruto)
        print(f"Total de questões identificadas: {len(questoes)}")
        
        if questoes:
            print(f"\n--- Exemplo: {questoes[0]['titulo']} ---")
            print(questoes[0]["conteudo"][:400])
    except Exception as e:
        print(f"Erro ao processar: {e}")
        