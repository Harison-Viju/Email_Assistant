import streamlit as st
import requests
import pandas as pd

API_BASE = st.secrets.get("API_BASE", "http://localhost:8000/api")

st.set_page_config(page_title="AI Support Assistant", layout="wide")
st.title("AI-Powered Communication Assistant")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Ingest Emails"):
        try:
            requests.post(f"{API_BASE}/emails/ingest")
        except Exception:
            st.error("Failed to ingest emails. Ensure backend is running.")
with col2:
    stats = {}
    try:
        stats = requests.get(f"{API_BASE}/emails/stats").json()
    except Exception:
        stats = {}
    st.metric("Total", stats.get("total", 0))
with col3:
    st.metric("Pending", stats.get("pending", 0))
with col4:
    st.metric("Drafted", stats.get("drafted", 0))
with col5:
    st.metric("Sent", stats.get("sent", 0))

st.subheader("Emails")
try:
    emails = requests.get(f"{API_BASE}/emails/").json()
except Exception:
    emails = []

if emails:
    df = pd.DataFrame(emails)
    st.dataframe(df[["id", "sender", "subject", "sentiment", "priority", "is_urgent", "status", "received_at"]], use_container_width=True)

    selected_id = st.selectbox("Select Email ID", options=df["id"].tolist())
    if selected_id:
        sel = next((e for e in emails if e["id"] == selected_id), None)
        if sel:
            st.write(f"From: {sel['sender']}")
            st.write(f"Subject: {sel['subject']}")
            st.write("Body:")
            st.code(sel.get("body", ""))
            st.write("Extracted Info:")
            st.json({
                "contact": sel.get("extracted_contact"),
                "requirements": sel.get("extracted_requirements"),
                "indicators": sel.get("extracted_indicators"),
            })

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Analyze", key="analyze"):
                    requests.post(f"{API_BASE}/emails/{selected_id}/analyze")
                    st.experimental_rerun()
            with c2:
                if st.button("Draft Reply", key="draft"):
                    r = requests.post(f"{API_BASE}/emails/{selected_id}/draft").json()
                    st.session_state["draft"] = r.get("draft")
            with c3:
                if st.button("Send Reply", key="send"):
                    requests.post(f"{API_BASE}/emails/{selected_id}/send")
                    st.success("Reply sent (if SMTP configured)")

            draft_text = st.text_area("Draft Reply", value=st.session_state.get("draft", ""), height=220)
            if st.button("Save Edited Draft"):
                # For brevity, not persisting edited draft via API update in this version
                st.session_state["draft"] = draft_text
                st.info("Draft updated locally.")
else:
    st.info("No emails loaded yet. Click 'Ingest Emails' or create via API.")


