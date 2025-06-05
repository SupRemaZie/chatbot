#!/bin/bash

set -e

echo "Lancement du serveur Ollama..."
ollama serve &

echo "Lancement de Streamlit..."
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
