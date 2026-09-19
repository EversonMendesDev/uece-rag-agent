import os
import chromadb
from google import genai
from sentence_transformers import SentenceTransformer

# Otimização de uso de memória no Windows
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

# 1. Conexão à base vetorial e modelo de embeddings
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="questoes_uece")
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")

# 2. Inicialização do cliente Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não foi definida no terminal.")

ai = genai.Client(api_key=api_key)

def recuperar_contexto(pergunta: str, top_k: int = 3) -> str:
    vetor = embedder.encode([pergunta]).tolist()
    resultados = collection.query(query_embeddings=vetor, n_results=top_k)
    
    contextos = []
    for i, doc in enumerate(resultados["documents"][0]):
        titulo = resultados["metadatas"][0][i]["titulo"]
        contextos.append(f"[{titulo}]\n{doc}")
        
    return "\n\n".join(contextos)

def responder_como_tutor(pergunta: str) -> str:
    contexto = recuperar_contexto(pergunta)
    
    prompt = f"""
Você é um tutor pedagógico amigável e especialista no vestibular da UECE. 
Sua missão é ensinar o estudante, explicando conceitos e guiando o raciocínio com base no material fornecido.

Diretrizes de resposta:
- Responda diretamente à dúvida usando o contexto fornecido.
- Explique o conceito teórico fundamental presente na questão.
- Dê uma dica estratégica de prova ou fixação de conteúdo para a UECE.
- Mantenha um tom encorajador, claro e didático.

--- CONTEXTO EXTRAÍDO DA PROVA ---
{contexto}

--- DÚVIDA DO ESTUDANTE ---
{pergunta}

Resposta do Tutor:
"""
    
    response = ai.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text

if __name__ == "__main__":
    print("🎓 Tutor Virtual UECE - Pronto para tirar dúvidas!")
    print("Digite sua pergunta sobre os temas da prova ou 'sair' para encerrar.\n" + "="*60)
    
    while True:
        pergunta = input("\nVocê: ")
        
        if pergunta.lower().strip() in ["sair", "exit", "quit"]:
            print("\n🎓 Tutor: Bons estudos e até a próxima! Foco na aprovação!")
            break
            
        if pergunta.strip():
            print("\n🎓 Tutor pensando...")
            resposta = responder_como_tutor(pergunta)
            print(f"\n🎓 Tutor:\n{resposta}")
            print("-" * 60)