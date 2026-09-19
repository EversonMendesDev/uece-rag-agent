import os
# Garante limites de memória no Windows
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import chromadb
from embedder import gerar_embeddings_questoes
from parser import extrair_texto_pdf
from chunker import separar_questoes

def salvar_questoes_no_banco():
    # Cria/Conecta ao banco vetorial salvo na pasta local 'chroma_db'
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Cria ou recupera a coleção de questões
    collection = client.get_or_create_collection(
        name="questoes_uece",
        metadata={"hnsw:space": "cosine"}
    )
    
    caminho_pdf = "../data/prova_uece.pdf"
    print("Extracting PDF text...")
    texto_bruto = extrair_texto_pdf(caminho_pdf)
    
    print("Chunking questions...")
    questoes = separar_questoes(texto_bruto)
    
    if not questoes:
        print("Nenhuma questão encontrada.")
        return

    print("Generating embeddings...")
    questoes_processadas = gerar_embeddings_questoes(questoes)
    
    # Prepara os dados para inserção no ChromaDB
    ids = [f"q_{i+1}" for i in range(len(questoes_processadas))]
    documents = [q["conteudo"] for q in questoes_processadas]
    embeddings = [q["embedding"] for q in questoes_processadas]
    metadatas = [{"titulo": q["titulo"]} for q in questoes_processadas]
    
    print(f"Salvando {len(questoes_processadas)} questões no ChromaDB local...")
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    print("\n✅ Sucesso! Todas as questões e vetores foram gravados na pasta 'backend/chroma_db' sem depender do Docker!")

if __name__ == "__main__":
    try:
        salvar_questoes_no_banco()
    except Exception as e:
        print(f"Erro no processamento: {e}")