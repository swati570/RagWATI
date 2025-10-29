import streamlit as st
from auth import login, register
from utils import upload_pdf, get_projects, ask_question, delete_project

st.set_page_config(page_title="PDF Chatbot", layout="wide")

with open("background.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("📚 PDF Chatbot Assistant")

if "token" not in st.session_state:
    st.session_state.token = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Login/Register
if st.session_state.token is None:
    choice = st.radio("Login or Register", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button(choice):
        if choice == "Login":
            token = login(username, password)
            if token:
                st.session_state.token = token
                st.success("Logged in!")
            else:
                st.error("Login failed")
        else:
            st.write(register(username, password))
else:
    st.success("Logged in!")

    # Project selection
    st.subheader("📁 Project & PDF Upload")
    project_id = st.text_input("Enter a Project ID")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file and st.button("Upload PDF"):
        result = upload_pdf(st.session_state.token, project_id, uploaded_file)
        st.write(result)

    # Project dropdown
    projects = get_projects(st.session_state.token)
    if projects:
        selected_project = st.selectbox("Select a Project", projects)
    else:
        selected_project = None
        st.info("No projects found. Upload a PDF to create one.")

    # Chatbot
    if selected_project:
        st.subheader("💬 Ask Questions")
        question = st.text_input("Your question")
        if st.button("Ask"):
            answer = ask_question(st.session_state.token, selected_project, question)
            st.session_state.chat_history.append(("You", question))
            st.session_state.chat_history.append(("Bot", answer))

        for speaker, msg in st.session_state.chat_history:
            st.markdown(f"**{speaker}:** {msg}")

        # Delete project
        if st.button("🗑️ Delete Project"):
            result = delete_project(st.session_state.token, selected_project)
            st.write(result)
