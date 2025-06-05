import streamlit as st
from pdf_reader import lire_pdf
from ollama_client import interroger_ollama
from vector_store import construire_vecteurs
import os

PDF_PATH = "SANOFI-Integrated-Annual-Report-2022-EN.pdf"

@st.cache_resource
def charger_vecteurs(path, file_modified_time):
    texte = lire_pdf(path)
    vecteurs = construire_vecteurs(texte)
    return texte, vecteurs

# === Titre / config ===
st.set_page_config(
    page_title="📄🔎 Chatbot PDF",
    layout="wide",      
    initial_sidebar_state="expanded" 
)
st.title("📄🔎 Chatbot PDF ")


with st.sidebar:
    st.header("⚙️ Paramètres")
    model = st.selectbox("Choisir le modèle Ollama", options=["mistral", "llama3.2", "nomic"], index=0)
    k = st.slider("Nombre de documents retournés (k)", min_value=1, max_value=10, value=4)
    reset_conv = st.button("🔄 Réinitialiser la conversation")

# Réinitialisation de la conversation
if reset_conv:
    st.session_state.messages = []
    st.rerun()


# === Initialisation session ===
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vecteurs" not in st.session_state:
    file_modified_time = os.path.getmtime(PDF_PATH)
    with st.spinner("📄 Chargement et indexation du PDF..."):
        texte, vecteurs = charger_vecteurs(PDF_PATH, file_modified_time)
        st.session_state.texte_pdf_text = texte
        st.session_state.vecteurs = vecteurs

# Affichage historique chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input utilisateur
question = st.chat_input("Pose une question sur le document PDF...")

if question:
    st.chat_message("user").markdown(question)
    st.session_state.messages.append({"role": "user", "content": question})

    # Recherche sémantique
    docs = st.session_state.vecteurs.similarity_search(question, k=k)
    contexte = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Tu es un assistant intelligent. Voici des extraits d'un PDF :

\"\"\"{contexte}\"\"\"

Réponds précisément à cette question en français : {question}
Ne réponds que sur la base du contexte ci-dessus.
"""
    with st.spinner("⏳ L'assistant réfléchit..."):
        reponse = interroger_ollama(prompt, modele=model)
        with st.chat_message("assistant"):
            st.markdown(reponse, unsafe_allow_html=False)



        st.session_state.messages.append({"role": "assistant", "content": reponse})



