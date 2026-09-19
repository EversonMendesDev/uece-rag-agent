import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import chromadb
from sentence_transformers import SentenceTransformer

# Conecta à base de dados vetorial local
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="questoes_uece")

# Carrega o mesmo modelo leve utilizado na indexação
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME, device="cpu")

def buscar_questoes(pergunta: str, n_resultados: int = 3):
    # Gera o vetor numérico da consulta
    vetor_consulta = model.encode([pergunta]).tolist()
    
    # Executa a pesquisa por similaridade de cosseno
    resultados = collection.query(
        query_embeddings=vetor_consulta,
        n_results=n_resultados
    )
    return resultados

if __name__ == "__main__":
    # Teste com uma busca sobre o tema da prova
    consulta = "figura de linguagem e metafora no texto"
    print(f"Pesquisando por: '{consulta}'...\n")
    
    res = buscar_questoes(consulta, n_resultados=2)
    
    for i, doc in enumerate(res["documents"][0]):
        titulo = res["metadatas"][0][i]["titulo"]
        distancia = res["distances"][0][i]
        print(f"--- Resultado {i+1}: {titulo} (Distância: {distancia:.4f}) ---")
        print(f"{doc[:350]}...\n")