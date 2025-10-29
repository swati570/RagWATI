import os
import uuid
from Backend.db_mongo import pdfs_col, chunks_col
from Backend.db_neo4j import graph
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from dotenv import load_dotenv
import numpy as np

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploaded_pdfs")
MAX_PDFS = int(os.getenv("MAX_PDFS_PER_PROJECT", "2"))

def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"
    return text

def generate_embedding(text):
    embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    embeddings = OllamaEmbeddings(model=embed_model)
    return embeddings.embed_query(text)

async def save_pdf(file, project_id, user_id):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    count = pdfs_col.count_documents({"project_id": project_id})
    if count >= MAX_PDFS:
        return {"error": "You can upload only 2 PDFs per project"}

    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(text)

    pdf_doc = {"project_id": project_id, "user_id": user_id, "path": path, "filename": file.filename}
    pdf_id = str(pdfs_col.insert_one(pdf_doc).inserted_id)

    chunk_docs = []
    for i, chunk in enumerate(chunks):
        emb = generate_embedding(chunk)
        chunk_docs.append({"pdf_id": pdf_id, "project_id": project_id, "text": chunk, "embedding": emb, "index": i})
    chunks_col.insert_many(chunk_docs)

    try:
        graph.run("MERGE (p:Project {id: $pid})", pid=project_id)
        graph.run("CREATE (d:PDF {id: $pdfid, name: $name})", pdfid=pdf_id, name=file.filename)
        graph.run("MATCH (p:Project {id: $pid}), (d:PDF {id: $pdfid}) MERGE (p)-[:HAS_PDF]->(d)",
                  pid=project_id, pdfid=pdf_id)
    except Exception as e:
        print("Neo4j error:", e)

    return {"message": "PDF processed", "pdf_id": pdf_id, "chunks": len(chunks)}

def delete_pdf(pdf_id):
    pdf = pdfs_col.find_one({"_id": pdf_id})
    if not pdf:
        return {"error": "PDF not found"}

    chunks_col.delete_many({"pdf_id": pdf_id})
    pdfs_col.delete_one({"_id": pdf_id})

    try:
        graph.run("MATCH (d:PDF {id: $pdfid}) DETACH DELETE d", pdfid=pdf_id)
    except Exception as e:
        print("Neo4j delete error:", e)

    path = pdf.get("path")
    if path and os.path.exists(path):
        os.remove(path)

    return {"status": "deleted"}

def get_user_projects(user_id):
    return pdfs_col.distinct("project_id", {"user_id": user_id})
