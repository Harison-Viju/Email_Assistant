#!/usr/bin/env python3
"""
Test script to demonstrate the AI-Powered Communication Assistant
"""

import requests
import json
from datetime import datetime

# Test data
test_emails = [
    {
        "sender": "customer1@example.com",
        "subject": "Support needed for login issue",
        "body": "Hi team, I am unable to log into my account since yesterday. Could you please help me resolve this issue? This is urgent as I need to access my data immediately.",
        "received_at": datetime.now().isoformat()
    },
    {
        "sender": "customer2@example.com", 
        "subject": "Query about product pricing",
        "body": "Hello, I wanted to understand the pricing tiers better. Could you share a detailed breakdown? Thanks!",
        "received_at": datetime.now().isoformat()
    },
    {
        "sender": "customer3@example.com",
        "subject": "Critical help needed for downtime", 
        "body": "Our servers are down, and we need immediate support. This is highly critical and affecting our operations.",
        "received_at": datetime.now().isoformat()
    }
]

def test_api():
    base_url = "http://localhost:8000"
    
    print("🚀 Testing AI-Powered Communication Assistant")
    print("=" * 50)
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Create test emails
    print("\n📧 Creating test emails...")
    created_emails = []
    for email in test_emails:
        try:
            response = requests.post(f"{base_url}/api/emails/", json=email)
            if response.status_code == 200:
                created_emails.append(response.json())
                print(f"✅ Created email from {email['sender']}")
            else:
                print(f"❌ Failed to create email: {response.text}")
        except Exception as e:
            print(f"❌ Error creating email: {e}")
    
    if not created_emails:
        print("❌ No emails created, cannot continue testing")
        return
    
    # Analyze emails
    print("\n🔍 Analyzing emails...")
    for email in created_emails:
        try:
            response = requests.post(f"{base_url}/api/emails/{email['id']}/analyze")
            if response.status_code == 200:
                analyzed = response.json()
                print(f"✅ Analyzed email {email['id']}: {analyzed['sentiment']} sentiment, {analyzed['priority']} priority")
            else:
                print(f"❌ Failed to analyze email {email['id']}: {response.text}")
        except Exception as e:
            print(f"❌ Error analyzing email {email['id']}: {e}")
    
    # Generate drafts
    print("\n✍️ Generating reply drafts...")
    for email in created_emails:
        try:
            response = requests.post(f"{base_url}/api/emails/{email['id']}/draft")
            if response.status_code == 200:
                draft = response.json()
                print(f"✅ Generated draft for email {email['id']}")
                print(f"   Draft preview: {draft['draft'][:100]}...")
            else:
                print(f"❌ Failed to generate draft for email {email['id']}: {response.text}")
        except Exception as e:
            print(f"❌ Error generating draft for email {email['id']}: {e}")
    
    # Get stats
    print("\n📊 Getting statistics...")
    try:
        response = requests.get(f"{base_url}/api/emails/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistics: {json.dumps(stats, indent=2)}")
        else:
            print(f"❌ Failed to get stats: {response.text}")
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
    
    # List all emails
    print("\n📋 Listing all emails...")
    try:
        response = requests.get(f"{base_url}/api/emails/")
        if response.status_code == 200:
            emails = response.json()
            print(f"✅ Found {len(emails)} emails:")
            for email in emails:
                print(f"   - ID: {email['id']}, From: {email['sender']}, Subject: {email['subject']}")
                print(f"     Sentiment: {email['sentiment']}, Priority: {email['priority']}, Urgent: {email['is_urgent']}")
        else:
            print(f"❌ Failed to list emails: {response.text}")
    except Exception as e:
        print(f"❌ Error listing emails: {e}")
    
    print("\n🎉 Test completed!")
    print("\nTo view the dashboard, run:")
    print("streamlit run backend/app/dashboard.py")

if __name__ == "__main__":
    test_api()

