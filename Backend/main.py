from fastapi import FastAPI, UploadFile, Form
from Backend.auth import router as auth_router
from Backend.services_pdf import save_pdf, delete_pdf
from Backend.services_query import get_answer
from Backend.utils import decode_jwt_token
from Backend.db_mongo import pdfs_col  

app = FastAPI(title="RagWATI")

app.include_router(auth_router, prefix="/auth")



@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile, project_id: str = Form(...), token: str = Form(...)):
    user = decode_jwt_token(token)
    if not user:
        return {"error": "Invalid token"}

    user_id = user["user_id"]

    # Check how many PDFs this user has already uploaded
    pdf_count = pdfs_col.count_documents({"user_id": user_id})
    if pdf_count >= 2:
        return {"error": "Upload limit reached (2 PDFs max)"}

    return await save_pdf(file, project_id, user_id)


@app.post("/ask")
def ask(project_id: str = Form(...), question: str = Form(...)):
    return {"answer": get_answer(project_id, question)}

@app.delete("/delete_pdf")
def delete_pdf_api(pdf_id: str, token: str):
    user = decode_jwt_token(token)
    if not user:
        return {"error": "Invalid token"}
    return delete_pdf(pdf_id)

