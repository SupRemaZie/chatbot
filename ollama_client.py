import requests
import streamlit as st
import json

def interroger_ollama(prompt, modele):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": modele,
        "prompt": prompt,
        "stream": True
    }

    try:
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()

        # Streamlit container pour afficher progressivement
        placeholder = st.empty()
        full_response = ""
        
        # Lecture des morceaux en temps réel
        for line in response.iter_lines():
            if line:
                try:
                    json_chunk = json.loads(line.decode("utf-8").strip().removeprefix("data: "))
                    content_piece = json_chunk.get("response", "")
                    full_response += content_piece
                    placeholder.markdown(full_response + "▌")  # curseur simulé
                except Exception:
                    continue
        placeholder.empty()
        return full_response

    except requests.RequestException as e:
        return f"Erreur lors de la requête Ollama (streaming) : {e}"
