import numpy as np
from Backend.db_mongo import chunks_col, pdfs_col
from langchain_ollama import OllamaLLM
from Backend.services_pdf import generate_embedding, get_user_projects

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def retrieve_chunks(project_id, query, k=3):
    q_emb = generate_embedding(query)
    chunks = list(chunks_col.find({"project_id": project_id}))
    scored = []
    for c in chunks:
        score = cosine_similarity(q_emb, c["embedding"])
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for s, c in scored[:k]]

def get_answer(project_id, question):
    top_chunks = retrieve_chunks(project_id, question)
    context = "\n".join([c["text"] for c in top_chunks])
    model_name = "llama3"
    llm = OllamaLLM(model=model_name)
    prompt = f"Use the following context to answer the question:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = llm.invoke(prompt)
    return response

def list_projects_for_user(user_id):
    return get_user_projects(user_id)

