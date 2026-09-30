import os
import re
import requests
import streamlit as st
from dotenv import load_dotenv
from utils.formatters import sanitize_text, format_docx, format_pdf, format_html_preview

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="centered")
st.markdown("<h1 style='text-align:center'>⚖️ LegalEase</h1><h3 style='text-align:center'>AI Legal Document Generator</h3>", unsafe_allow_html=True)
st.info("AI-generated legal drafts can contain errors and may not satisfy local law. Review the final document with a qualified legal professional before relying on it.")

with st.form("legal_form"):
    document_type = st.selectbox("Document Type", ["Employment Contract", "Non-Disclosure Agreement (NDA)", "Residential Lease Agreement", "Freelance Work Contract", "Service Agreement", "Other"])
    if document_type == "Other": document_type = st.text_input("Enter document type")
    parties = st.text_area("Parties Involved", placeholder="Jane Doe (Service Provider); TechNova Inc. (Client)")
    terms = st.text_area("Terms & Conditions", placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice")
    dates = st.text_input("Effective Date(s)", placeholder="April 15, 2026")
    submitted = st.form_submit_button("Generate Document", use_container_width=True)

if submitted:
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please complete all fields.")
    else:
        try:
            with st.spinner("Generating document..."):
                r = requests.post(f"{BACKEND_URL}/generate", json={"document_type": document_type, "parties": parties, "terms": terms, "dates": dates}, timeout=120)
                r.raise_for_status(); st.session_state.generated_text = sanitize_text(r.json()["document"]); st.session_state.doc_type = document_type
        except requests.RequestException as exc:
            detail = getattr(exc.response, "text", "") if getattr(exc, "response", None) is not None else ""
            st.error(f"Backend request failed. Ensure FastAPI is running and the Gemini key is configured. {detail}")

if st.session_state.get("generated_text"):
    st.success("Document generated successfully.")
    st.markdown(format_html_preview(st.session_state.generated_text), unsafe_allow_html=True)
    edited = st.text_area("Edit Document Below", st.session_state.generated_text, height=420)
    st.session_state.generated_text = edited
    name = re.sub(r"[^A-Za-z0-9_-]+", "_", st.session_state.doc_type).strip("_").lower() or "legal_document"
    c1, c2, c3 = st.columns(3)
    with c1: st.download_button("Download TXT", edited.encode("utf-8"), f"{name}.txt", "text/plain", use_container_width=True)
    with c2: st.download_button("Download DOCX", format_docx(edited, st.session_state.doc_type), f"{name}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with c3: st.download_button("Download PDF", format_pdf(edited, st.session_state.doc_type), f"{name}.pdf", "application/pdf", use_container_width=True)
