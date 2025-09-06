import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000/api"

st.set_page_config(page_title="AI Support Assistant", layout="wide")
st.title("🤖 AI-Powered Communication Assistant")
st.markdown("---")

# Header with action buttons
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("📥 Ingest Emails", type="primary"):
        try:
            response = requests.post(f"{API_BASE}/emails/ingest")
            if response.status_code == 200:
                st.success("Emails ingested successfully!")
            else:
                st.error("Failed to ingest emails.")
        except Exception as e:
            st.error(f"Failed to ingest emails: {e}")

# Get stats
stats = {}
try:
    stats = requests.get(f"{API_BASE}/emails/stats").json()
except Exception:
    stats = {}

with col2:
    st.metric("📊 Total Emails", stats.get("total", 0))
with col3:
    st.metric("⏳ Pending", stats.get("pending", 0))
with col4:
    st.metric("✍️ Drafted", stats.get("drafted", 0))
with col5:
    st.metric("📤 Sent", stats.get("sent", 0))

# Analytics Section
st.markdown("## 📈 Analytics Dashboard")

# Get emails for analytics
try:
    emails = requests.get(f"{API_BASE}/emails/").json()
except Exception:
    emails = []

if emails:
    df = pd.DataFrame(emails)
    
    # Convert received_at to datetime
    df['received_at'] = pd.to_datetime(df['received_at'], errors='coerce')
    
    # Analytics columns
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment distribution
        sentiment_counts = df['sentiment'].value_counts()
        fig_sentiment = px.pie(
            values=sentiment_counts.values, 
            names=sentiment_counts.index,
            title="Sentiment Distribution",
            color_discrete_map={'positive': '#2E8B57', 'negative': '#DC143C', 'neutral': '#4682B4'}
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        # Priority distribution
        priority_counts = df['priority'].value_counts()
        fig_priority = px.bar(
            x=priority_counts.index, 
            y=priority_counts.values,
            title="Priority Distribution",
            color=priority_counts.index,
            color_discrete_map={'urgent': '#FF6B6B', 'not_urgent': '#4ECDC4'}
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    # Time-based analytics
    if not df['received_at'].isna().all():
        df['hour'] = df['received_at'].dt.hour
        hourly_counts = df.groupby('hour').size().reset_index(name='count')
        
        fig_timeline = px.line(
            hourly_counts, 
            x='hour', 
            y='count',
            title="Emails Received by Hour",
            markers=True
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

# Email Management Section
st.markdown("## 📧 Email Management")

# Get emails for management
try:
    emails = requests.get(f"{API_BASE}/emails/").json()
except Exception:
    emails = []

if emails:
    df = pd.DataFrame(emails)
    
    # Priority-based sorting (urgent first)
    df = df.sort_values(['is_urgent', 'received_at'], ascending=[False, False])
    
    # Display emails in a nice format
    for idx, email in df.iterrows():
        with st.expander(f"🚨 {email['subject']} - {email['sender']} ({email['priority']})" if email['is_urgent'] else f"📧 {email['subject']} - {email['sender']} ({email['priority']})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**From:** {email['sender']}")
                st.write(f"**Subject:** {email['subject']}")
                st.write(f"**Received:** {email['received_at']}")
                st.write(f"**Status:** {email['status']}")
                
                # Sentiment and Priority badges
                sentiment_color = "🟢" if email['sentiment'] == 'positive' else "🔴" if email['sentiment'] == 'negative' else "🟡"
                priority_color = "🔴" if email['is_urgent'] else "🟢"
                st.write(f"**Sentiment:** {sentiment_color} {email['sentiment']} | **Priority:** {priority_color} {email['priority']}")
                
                st.write("**Email Body:**")
                st.text_area("", value=email.get("body", ""), height=100, disabled=True, key=f"body_{email['id']}")
                
                # Extracted Information
                if email.get("extracted_contact") or email.get("extracted_requirements") or email.get("extracted_indicators"):
                    st.write("**Extracted Information:**")
                    if email.get("extracted_contact"):
                        st.write(f"📞 Contact: {email['extracted_contact']}")
                    if email.get("extracted_requirements"):
                        st.write(f"📋 Requirements: {email['extracted_requirements']}")
                    if email.get("extracted_indicators"):
                        st.write(f"🔍 Indicators: {email['extracted_indicators']}")
            
            with col2:
                st.write("**Actions:**")
                
                if st.button("🔍 Analyze", key=f"analyze_{email['id']}"):
                    try:
                        response = requests.post(f"{API_BASE}/emails/{email['id']}/analyze")
                        if response.status_code == 200:
                            st.success("Email analyzed!")
                            st.rerun()
                        else:
                            st.error("Analysis failed")
                    except Exception as e:
                        st.error(f"Error: {e}")
                
                if st.button("✍️ Draft Reply", key=f"draft_{email['id']}"):
                    try:
                        response = requests.post(f"{API_BASE}/emails/{email['id']}/draft")
                        if response.status_code == 200:
                            draft_data = response.json()
                            st.session_state[f"draft_{email['id']}"] = draft_data.get("draft", "")
                            st.success("Draft generated!")
                        else:
                            st.error("Draft generation failed")
                    except Exception as e:
                        st.error(f"Error: {e}")
                
                if st.button("📤 Send Reply", key=f"send_{email['id']}"):
                    try:
                        response = requests.post(f"{API_BASE}/emails/{email['id']}/send")
                        if response.status_code == 200:
                            st.success("Reply sent!")
                        else:
                            st.error("Send failed")
                    except Exception as e:
                        st.error(f"Error: {e}")
                
                # Draft editing
                draft_key = f"draft_{email['id']}"
                if draft_key not in st.session_state:
                    st.session_state[draft_key] = ""
                
                draft_text = st.text_area(
                    "Edit Draft:", 
                    value=st.session_state[draft_key], 
                    height=150, 
                    key=f"edit_draft_{email['id']}"
                )
                
                if st.button("💾 Save Draft", key=f"save_{email['id']}"):
                    st.session_state[draft_key] = draft_text
                    st.success("Draft saved!")
            
            st.markdown("---")

else:
    st.info("📭 No emails loaded yet. Click 'Ingest Emails' to load sample emails or configure real email integration.")
    
    # Show sample data preview
    st.markdown("### 🎯 Sample Data Preview")
    st.code("""
    The system will automatically load sample emails for demonstration:
    - Support needed for login issue (URGENT)
    - Query about product pricing (Normal)
    - Critical help needed for downtime (URGENT)
    """)


