from langchain_community.document_loaders import PyPDFLoader

import tempfile
import os
def lire_pdf(file_path):
    with open(file_path, "rb") as f:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(f.read())
            tmp.flush()
            tmp_path = tmp.name

    try:
        loader = PyPDFLoader(tmp_path)
        documents = loader.load()
        texte = "\n".join([doc.page_content for doc in documents])
    finally:
        os.remove(tmp_path)

    return texte

