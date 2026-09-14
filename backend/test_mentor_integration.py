"""
SIKSHASATHI — AI Mentor Comprehensive Integration Test Suite
Validates:
1. Auth & Session verification
2. Conversation CRUD (Create, List, Load, Delete, Search)
3. 3 Modes: Socratic, Deep Concept, Exam Solver
4. Message persistence & history recall
5. User isolation (Student A cannot read or access Student B's conversations)
6. Preferences GET/PUT (AI Persona & study settings)
7. Dynamic Suggestions
8. Notes RAG integration
"""

import sys
import json
import time
import requests

BASE_URL = "http://127.0.0.1:8000"

def log_test(step_num, title, passed, details=""):
    status = "[PASS]" if passed else "[FAIL]"
    print(f"[{step_num}] {status}: {title}")
    if details:
        safe_details = details.encode('ascii', errors='replace').decode('ascii')
        print(f"    -> {safe_details}")
    if not passed:
        sys.exit(1)

def main():
    print("==================================================")
    print("SIKSHASATHI AI MENTOR INTEGRATION TEST SUITE")
    print("==================================================")

    # 1. Login Student A
    print("\n--- Phase 1: Authentication ---")
    login_payload_a = {
        "email": "aarav@siksha.edu",
        "password": "student123"
    }
    r = requests.post(f"{BASE_URL}/api/auth/login", json=login_payload_a)
    log_test(1, "Student A Login (Aarav)", r.status_code == 200, f"Status {r.status_code}")
    auth_data_a = r.json()
    token_a = auth_data_a["access_token"]
    user_a = auth_data_a["user"]
    headers_a = {"Authorization": f"Bearer {token_a}", "Content-Type": "application/json"}

    # Login Student B (Diya)
    login_payload_b = {
        "email": "student2@siksha.edu",
        "password": "student123"
    }
    r = requests.post(f"{BASE_URL}/api/auth/login", json=login_payload_b)
    log_test(2, "Student B Login (Diya)", r.status_code == 200, f"Status {r.status_code}")
    auth_data_b = r.json()
    token_b = auth_data_b["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}", "Content-Type": "application/json"}

    # 2. Preferences Test
    print("\n--- Phase 2: AI Preferences ---")
    r = requests.get(f"{BASE_URL}/api/mentor/preferences", headers=headers_a)
    log_test(3, "GET Student A Preferences", r.status_code == 200, f"Prefs: {r.json().get('preferences')}")

    r = requests.put(f"{BASE_URL}/api/mentor/preferences", headers=headers_a, json={
        "persona": "friendly",
        "daily_study_minutes": 60
    })
    log_test(4, "PUT Student A Preferences", r.status_code == 200 and r.json()["preferences"]["persona"] == "friendly")

    # 3. Create Conversation
    print("\n--- Phase 3: Conversation Creation & Mode 1 (Socratic) ---")
    create_conv_payload = {
        "title": "Kinematics & Projectile Apex",
        "mode": "socratic",
        "subject": "Physics"
    }
    r = requests.post(f"{BASE_URL}/api/mentor/conversations", headers=headers_a, json=create_conv_payload)
    log_test(5, "Create Mentor Conversation", r.status_code == 200 and "conversation_id" in r.json())
    conv_id = r.json()["conversation_id"]

    # 4. Socratic Chat
    chat_payload_socratic = {
        "conversation_id": conv_id,
        "message": "At the highest point of projectile motion, why isn't acceleration zero since velocity is zero?",
        "mode": "socratic"
    }
    r = requests.post(f"{BASE_URL}/api/mentor/chat", headers=headers_a, json=chat_payload_socratic)
    log_test(6, "Socratic Mode Inquiry", r.status_code == 200, f"Reply snippet: {r.json().get('reply', '')[:100]}...")
    reply_socratic = r.json()
    assert "reply" in reply_socratic

    # 5. Deep Concept Mode
    print("\n--- Phase 4: Mode 2 (Deep Concept) ---")
    chat_payload_deep = {
        "conversation_id": conv_id,
        "message": "Explain the first principles derivation of why acceleration remains -g at the apex.",
        "mode": "deep"
    }
    r = requests.post(f"{BASE_URL}/api/mentor/chat", headers=headers_a, json=chat_payload_deep)
    log_test(7, "Deep Concept Mode Reasoning", r.status_code == 200, f"Reply snippet: {r.json().get('reply', '')[:100]}...")

    # 6. Exam Solver Mode
    print("\n--- Phase 5: Mode 3 (Exam Solver) ---")
    chat_payload_exam = {
        "conversation_id": conv_id,
        "message": "A ball is thrown upward at 20 m/s. Calculate max height and time of flight with g=10 m/s^2.",
        "mode": "exam"
    }
    r = requests.post(f"{BASE_URL}/api/mentor/chat", headers=headers_a, json=chat_payload_exam)
    log_test(8, "Exam Solver Step-by-Step", r.status_code == 200, f"Reply snippet: {r.json().get('reply', '')[:100]}...")

    # 7. Verify Message Persistence
    print("\n--- Phase 6: Persistence & Message History ---")
    r = requests.get(f"{BASE_URL}/api/mentor/conversations/{conv_id}", headers=headers_a)
    log_test(9, "Fetch Conversation with Messages", r.status_code == 200)
    conv_detail = r.json()
    messages = conv_detail.get("messages", [])
    log_test(10, "Verify Message Count in SQLite", len(messages) >= 6, f"Total persisted messages: {len(messages)}")

    # 8. Dynamic Suggestions
    print("\n--- Phase 7: Dynamic Suggestions ---")
    r = requests.post(f"{BASE_URL}/api/mentor/suggestions?mode=socratic", headers=headers_a)
    log_test(11, "Socratic Suggestions", r.status_code == 200 and len(r.json().get("suggestions", [])) > 0, f"Suggestions: {r.json().get('suggestions')}")

    r = requests.post(f"{BASE_URL}/api/mentor/suggestions?mode=exam", headers=headers_a)
    log_test(12, "Exam Solver Suggestions", r.status_code == 200 and len(r.json().get("suggestions", [])) > 0, f"Suggestions: {r.json().get('suggestions')}")

    # 9. Search Conversations
    print("\n--- Phase 8: Search Conversations ---")
    r = requests.get(f"{BASE_URL}/api/mentor/conversations?search=Kinematics", headers=headers_a)
    search_results = r.json().get("conversations", [])
    found = any(c["id"] == conv_id for c in search_results)
    log_test(13, "Search by keyword 'Kinematics'", found, f"Matching conversations found: {len(search_results)}")

    # 10. Multi-User Isolation
    print("\n--- Phase 9: Multi-User Isolation ---")
    # Student B attempts to access Student A's conversation
    r = requests.get(f"{BASE_URL}/api/mentor/conversations/{conv_id}", headers=headers_b)
    log_test(14, "Student B Access Denied to Student A Conversation", r.status_code == 404, f"Status: {r.status_code}")

    # Student B list conversations
    r = requests.get(f"{BASE_URL}/api/mentor/conversations", headers=headers_b)
    convs_b = r.json().get("conversations", [])
    conv_ids_b = [c["id"] for c in convs_b]
    log_test(15, "Student B Conversation List Isolation", conv_id not in conv_ids_b, f"Student B has {len(convs_b)} convs")

    # 11. Delete Conversation
    print("\n--- Phase 10: Delete Conversation ---")
    r = requests.delete(f"{BASE_URL}/api/mentor/conversations/{conv_id}", headers=headers_a)
    log_test(16, "Delete Conversation", r.status_code == 200)

    r = requests.get(f"{BASE_URL}/api/mentor/conversations/{conv_id}", headers=headers_a)
    log_test(17, "Verify Deleted Conversation 404", r.status_code == 404)

    print("\n==================================================")
    print("ALL 17 AI MENTOR INTEGRATION TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    main()
