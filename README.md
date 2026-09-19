# Agente de IA para o Vestibular da UECE 📚🤖

Plataforma RAG gratuita baseada em inteligência artificial para democratizar a preparação para o vestibular da UECE, voltada para estudantes da rede pública no Ceará.

## 🛠️ Stack Tecnológica
- **Parsing:** `pdfplumber`
- **Embeddings:** `sentence-transformers`
- **Base de Dados Vetorial:** PostgreSQL + `pgvector`
- **Backend:** FastAPI
- **Frontend:** React / Next.js

## 📋 Roadmap do Projeto
- [x] Configuração inicial do repositório e ambiente Docker
- [ ] Pipeline de extração de questões dos PDFs da UECE com `pdfplumber`
- [ ] Armazenamento vetorial e busca semântica com `pgvector`
- [ ] Endpoints da API assíncrona em FastAPI
- [ ] Interface Web *mobile-first* em Next.js