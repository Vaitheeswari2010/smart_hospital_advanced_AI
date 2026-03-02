import streamlit as st
import os
import pandas as pd
import torch
from datetime import datetime
import smtplib
from email.message import EmailMessage
import re

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    MarianMTModel,
    MarianTokenizer
)

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


SENTIMENT_MODEL_PATH = r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\genai\sentiment_model"
NEGATIVE_REPORT_PATH = "monthly_patient_negative.xlsx"

HR_EMAIL = "vaitheeswari0200@gmail.com"
SENDER_EMAIL = "hospitalgenai@gmail.com"
GMAIL_APP_PASSWORD = "nwms oteq kbjc hkrx"  # change


@st.cache_resource
def load_rag():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    patient_loader = PyPDFLoader(
        r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\genai\pdfs\final_patient_rag.pdf"
    )
    patient_docs = splitter.split_documents(patient_loader.load())
    patient_db = FAISS.from_documents(patient_docs, embeddings)

    staff_loader = PyPDFLoader(
        r"C:\Users\vaith\PycharmProjects\PythonProject\smart_hospital_advanced\genai\pdfs\staff_final_rag.pdf"
    )
    staff_docs = splitter.split_documents(staff_loader.load())
    staff_db = FAISS.from_documents(staff_docs, embeddings)

    return patient_db, staff_db


patient_db, staff_db = load_rag()


def detect_language(text):
    if re.search(r'[\u0900-\u097F]', text):
        return "hi"
    if re.search(r'[\u0D00-\u0D7F]', text):
        return "ml"
    return "en"


MODEL_MAP = {
    ("hi","en"): "Helsinki-NLP/opus-mt-hi-en",
    ("en","hi"): "Helsinki-NLP/opus-mt-en-hi",
    ("ml","en"): "Helsinki-NLP/opus-mt-ml-en",
    ("en","ml"): "Helsinki-NLP/opus-mt-en-ml",
}

_loaded_models = {}

def translate(text, src, tgt):
    if src == tgt:
        return text

    key = (src, tgt)
    if key not in MODEL_MAP:
        return text

    if key not in _loaded_models:
        tokenizer = MarianTokenizer.from_pretrained(MODEL_MAP[key])
        model = MarianMTModel.from_pretrained(MODEL_MAP[key])
        _loaded_models[key] = (tokenizer, model)

    tokenizer, model = _loaded_models[key]
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    output = model.generate(**tokens)
    return tokenizer.decode(output[0], skip_special_tokens=True)


def ask_rag(question_en, user_type="patient"):
    db = staff_db if user_type == "staff" else patient_db
    docs = db.similarity_search(question_en, k=3)
    return "\n\n".join(d.page_content for d in docs)


def multilingual_bot(question, user_type="patient"):
    src = detect_language(question)
    q_en = translate(question, src, "en")
    ans_en = ask_rag(q_en, user_type)
    return translate(ans_en, "en", src)


@st.cache_resource
def load_sentiment_model():
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_PATH)
    return tokenizer, model


def predict_sentiment(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    label = torch.argmax(outputs.logits).item()
    return "Positive" if label == 1 else "Negative"


def send_monthly_negative_report():
    if not os.path.exists(NEGATIVE_REPORT_PATH):
        return

    msg = EmailMessage()
    msg["Subject"] = "Monthly Negative Feedback Report"
    msg["From"] = SENDER_EMAIL
    msg["To"] = HR_EMAIL
    msg.set_content("Attached negative feedback report")

    with open(NEGATIVE_REPORT_PATH, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="negative_feedback.xlsx"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, GMAIL_APP_PASSWORD)
        server.send_message(msg)


def show_user_dashboard(user_name="User"):

    if "user_page" not in st.session_state:
        st.session_state.user_page = "chat"

    st.markdown("""
    <style>
    .navbar {
        background:#0b5394;
        padding:14px;
        color:white;
        font-size:18px;
        font-weight:bold;
        display:flex;
        justify-content:space-between;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="navbar">
        <div>🏥 Susila Multispeciality Hospital</div>
        <div>Welcome, {user_name}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💬 Chat with Me"):
            st.session_state.user_page = "chat"
    with c2:
        if st.button("📝 Feedback"):
            st.session_state.user_page = "feedback"
    with c3:
        if st.button("👤 Profile"):
            st.session_state.user_page = "profile"

    st.markdown("---")

    # ================= CHAT =================
    if st.session_state.user_page == "chat":
        st.subheader("💬 Chat with Me")

        question = st.text_input(
            "Ask your health question (English / Hindi / Malayalam)"
        )

        if st.button("🧠 Answer Me"):
            if question.strip():
                with st.spinner("Thinking..."):
                    answer = multilingual_bot(question, "patient")
                st.success(answer)

    # ================= FEEDBACK =================
    elif st.session_state.user_page == "feedback":
        st.subheader("📝 Patient Feedback")

        user_type = st.selectbox(
            "User Type", ["Patient", "Attender", "Visitor"]
        )

        department = st.selectbox(
            "Department",
            ["General Medicine","Cardiology","Neurology","Nephrology","ICU","Surgery"]
        )

        feedback = st.text_area("Your Feedback")

        if st.button("Submit Feedback"):
            if feedback.strip():
                tokenizer, model = load_sentiment_model()
                sentiment = predict_sentiment(feedback, tokenizer, model)

                df = pd.DataFrame([{
                    "Date": datetime.today().date(),
                    "User Type": user_type,
                    "Department": department,
                    "Feedback": feedback,
                    "Sentiment": sentiment
                }])

                if sentiment == "Negative":
                    if os.path.exists(NEGATIVE_REPORT_PATH):
                        old = pd.read_excel(NEGATIVE_REPORT_PATH)
                        df = pd.concat([old, df], ignore_index=True)
                    df.to_excel(NEGATIVE_REPORT_PATH, index=False)

                st.success(f"Saved ✅ | Sentiment: {sentiment}")

                if datetime.today().day == 1:
                    send_monthly_negative_report()

 
    else:
        st.subheader("👤 Profile")
        st.info("Profile module – next phase 🚧")
