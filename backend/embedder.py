import os

# Força o uso mínimo de memória e otimiza o PyTorch para CPU
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32"

from sentence_transformers import SentenceTransformer
from parser import extrair_texto_pdf
from chunker import separar_questoes

print("Carregando o modelo ultra-leve (~80 MB)...")
# Modelo compacto com 384 dimensões e baixo consumo de RAM
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME, device="cpu")

def gerar_embeddings_questoes(questoes: list[dict]) -> list[dict]:
    textos = [q["conteudo"] for q in questoes]
    
    print(f"Gerando embeddings para {len(textos)} questões...")
    # batch_size=2 reduz drasticamente o consumo de memória durante a inferência
    embeddings = model.encode(textos, show_progress_bar=True, batch_size=2)
    
    for i, questao in enumerate(questoes):
        questao["embedding"] = embeddings[i].tolist()
        
    return questoes

if __name__ == "__main__":
    caminho_pdf = "../data/prova_uece.pdf"
    try:
        texto_bruto = extrair_texto_pdf(caminho_pdf)
        questoes = separar_questoes(texto_bruto)
        
        if questoes:
            questoes_com_vector = gerar_embeddings_questoes(questoes)
            exemplo = questoes_com_vector[0]
            vector = exemplo["embedding"]
            
            print("\n--- Validação do Embedding ---")
            print(f"Título: {exemplo['titulo']}")
            print(f"Dimensão do vetor: {len(vector)}")
            print(f"Primeiros 5 valores do vetor: {vector[:5]}")
        else:
            print("Nenhuma questão para processar.")
    except Exception as e:
        print(f"Erro ao gerar embeddings: {e}")