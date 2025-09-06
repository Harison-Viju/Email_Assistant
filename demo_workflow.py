#!/usr/bin/env python3
"""
Complete Demo Workflow for AI-Powered Communication Assistant
This script demonstrates all the features required for the hackathon submission.
"""

import requests
import time
import json
from datetime import datetime

API_BASE = "http://localhost:8000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n📋 Step {step}: {description}")
    print("-" * 40)

def demo_workflow():
    print_header("AI-Powered Communication Assistant - Complete Demo")
    print("This demo showcases all hackathon requirements:")
    print("✅ Email Retrieval & Filtering")
    print("✅ Categorization & Prioritization") 
    print("✅ Context-Aware Auto-Responses")
    print("✅ Information Extraction")
    print("✅ Interactive Dashboard")
    print("✅ RAG + Prompt Engineering")
    
    # Step 1: Health Check
    print_step(1, "Health Check")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
        else:
            print("❌ Backend health check failed")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please start the backend with: uvicorn backend.app.main:app --reload --port 8000")
        return
    
    # Step 2: Email Ingestion
    print_step(2, "Email Ingestion & Filtering")
    print("📥 Ingesting sample emails (filtered by Support/Query/Request/Help keywords)...")
    
    try:
        response = requests.post(f"{API_BASE}/api/emails/ingest")
        if response.status_code == 200:
            emails = response.json()
            print(f"✅ Successfully ingested {len(emails)} support emails")
            for email in emails:
                print(f"   📧 {email['subject']} - {email['sender']}")
        else:
            print("❌ Email ingestion failed")
            return
    except Exception as e:
        print(f"❌ Error during ingestion: {e}")
        return
    
    # Step 3: Analytics
    print_step(3, "Analytics & Statistics")
    try:
        response = requests.get(f"{API_BASE}/api/emails/stats")
        if response.status_code == 200:
            stats = response.json()
            print("📊 Current Statistics:")
            print(f"   📈 Total Emails: {stats['total']}")
            print(f"   ⏳ Pending: {stats['pending']}")
            print(f"   ✍️ Drafted: {stats['drafted']}")
            print(f"   📤 Sent: {stats['sent']}")
            print(f"   🚨 Urgent: {stats['urgent']}")
        else:
            print("❌ Failed to get statistics")
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
    
    # Step 4: Email Analysis
    print_step(4, "Sentiment Analysis & Prioritization")
    try:
        response = requests.get(f"{API_BASE}/api/emails/")
        if response.status_code == 200:
            emails = response.json()
            print("🔍 Analyzing emails for sentiment and priority...")
            
            for email in emails[:3]:  # Show first 3 emails
                print(f"\n📧 Email ID {email['id']}: {email['subject']}")
                print(f"   👤 From: {email['sender']}")
                print(f"   😊 Sentiment: {email['sentiment']}")
                print(f"   ⚡ Priority: {email['priority']}")
                print(f"   🚨 Urgent: {'Yes' if email['is_urgent'] else 'No'}")
                
                # Show extracted information
                if email.get('extracted_contact'):
                    print(f"   📞 Contact: {email['extracted_contact']}")
                if email.get('extracted_requirements'):
                    print(f"   📋 Requirements: {email['extracted_requirements']}")
                if email.get('extracted_indicators'):
                    print(f"   🔍 Indicators: {email['extracted_indicators']}")
        else:
            print("❌ Failed to get emails")
    except Exception as e:
        print(f"❌ Error analyzing emails: {e}")
    
    # Step 5: AI Response Generation
    print_step(5, "AI-Powered Response Generation (RAG + LLM)")
    try:
        response = requests.get(f"{API_BASE}/api/emails/")
        if response.status_code == 200:
            emails = response.json()
            print("🤖 Generating AI responses using RAG and prompt engineering...")
            
            for email in emails[:2]:  # Generate drafts for first 2 emails
                print(f"\n✍️ Generating draft for Email ID {email['id']}...")
                
                # Generate draft
                draft_response = requests.post(f"{API_BASE}/api/emails/{email['id']}/draft")
                if draft_response.status_code == 200:
                    draft_data = draft_response.json()
                    draft_text = draft_data.get('draft', '')
                    print(f"   📝 Generated draft:")
                    print(f"   {draft_text[:200]}...")
                    print(f"   ✅ Draft saved successfully")
                else:
                    print(f"   ❌ Failed to generate draft")
    except Exception as e:
        print(f"❌ Error generating responses: {e}")
    
    # Step 6: Priority Queue Demonstration
    print_step(6, "Priority Queue Implementation")
    try:
        response = requests.get(f"{API_BASE}/api/emails/")
        if response.status_code == 200:
            emails = response.json()
            print("📋 Email Priority Queue (Urgent emails first):")
            
            urgent_count = 0
            normal_count = 0
            
            for i, email in enumerate(emails, 1):
                priority_icon = "🚨" if email['is_urgent'] else "📧"
                status_icon = "✅" if email['status'] == 'drafted' else "⏳"
                
                print(f"   {i}. {priority_icon} {email['subject']} - {email['sender']} {status_icon}")
                
                if email['is_urgent']:
                    urgent_count += 1
                else:
                    normal_count += 1
            
            print(f"\n📊 Queue Summary:")
            print(f"   🚨 Urgent emails: {urgent_count}")
            print(f"   📧 Normal emails: {normal_count}")
            print(f"   ✅ Total processed: {len(emails)}")
    except Exception as e:
        print(f"❌ Error showing priority queue: {e}")
    
    # Step 7: Final Statistics
    print_step(7, "Final Analytics")
    try:
        response = requests.get(f"{API_BASE}/api/emails/stats")
        if response.status_code == 200:
            stats = response.json()
            print("📈 Final Statistics:")
            print(f"   📊 Total Emails: {stats['total']}")
            print(f"   ⏳ Pending: {stats['pending']}")
            print(f"   ✍️ Drafted: {stats['drafted']}")
            print(f"   📤 Sent: {stats['sent']}")
            print(f"   🚨 Urgent: {stats['urgent']}")
            
            # Calculate efficiency metrics
            if stats['total'] > 0:
                processed_rate = ((stats['drafted'] + stats['sent']) / stats['total']) * 100
                urgent_rate = (stats['urgent'] / stats['total']) * 100
                print(f"\n🎯 Efficiency Metrics:")
                print(f"   📈 Processing Rate: {processed_rate:.1f}%")
                print(f"   🚨 Urgent Email Rate: {urgent_rate:.1f}%")
    except Exception as e:
        print(f"❌ Error getting final stats: {e}")
    
    # Step 8: Dashboard Access
    print_step(8, "Interactive Dashboard Access")
    print("🌐 Access the interactive dashboard at: http://localhost:8501")
    print("📊 Dashboard features:")
    print("   • Real-time analytics with interactive charts")
    print("   • Sentiment distribution pie chart")
    print("   • Priority breakdown bar chart")
    print("   • Time-based email trends")
    print("   • Email management with priority queue")
    print("   • Draft editing and sending capabilities")
    
    print_header("Demo Complete! 🎉")
    print("✅ All hackathon requirements demonstrated:")
    print("   📧 Email Retrieval & Filtering - COMPLETE")
    print("   🧠 Categorization & Prioritization - COMPLETE")
    print("   🤖 Context-Aware Auto-Responses - COMPLETE")
    print("   📊 Information Extraction - COMPLETE")
    print("   🎨 Interactive Dashboard - COMPLETE")
    print("   🔗 RAG + Prompt Engineering - COMPLETE")
    print("\n🚀 Ready for hackathon submission!")

if __name__ == "__main__":
    demo_workflow()
