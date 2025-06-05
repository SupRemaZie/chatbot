from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
import time
import streamlit as st

@st.cache_resource(show_spinner="🔄 Indexation du document en cours...")
def construire_vecteurs(texte, persist_dir="chroma_db"):
    # 1. Split optimisé
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,        # réduit taille pour réponses + ciblées
        chunk_overlap=100      # moins de redondance
    )
    textes = splitter.split_text(texte)

    # 2. Nettoyage facultatif
    textes = [t for t in textes if len(t.strip()) > 200]  # ignore les très courts

    # 3. Embeddings performants
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # 4. Timer pour log perf
    start = time.time()
    vecteurs = Chroma.from_texts(
        textes,
        embedding=embeddings,
        persist_directory=persist_dir
    )
    duration = time.time() - start
    print(f"✅ Vecteurs construits en {duration:.2f}s avec {len(textes)} chunks")

    return vecteurs
