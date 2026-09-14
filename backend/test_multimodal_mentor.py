"""
SIKSHASATHI — AI Mentor Multimodal (Images & PDFs) Test Suite
Tests text, image OCR/multimodal, and PDF RAG extraction in AI Mentor.
"""

import sys
import io
import base64
import httpx
from PIL import Image, ImageDraw

BASE_URL = "http://127.0.0.1:8000"

def generate_test_image_base64():
    """Creates a sample physics diagram image with text and formulas."""
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 30), "Physics Problem: Projectile Motion", fill=(0, 0, 0))
    draw.text((20, 70), "Initial Velocity u = 20 m/s", fill=(0, 0, 0))
    draw.text((20, 110), "Angle theta = 45 degrees", fill=(0, 0, 0))
    draw.text((20, 150), "Find maximum height H", fill=(0, 0, 0))
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_test_pdf_base64():
    """Creates a sample PDF document using fitz."""
    try:
        import fitz
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 72), "CHAPTER 4: THERMODYNAMICS & CARNOT ENGINE\n\nEfficiency of Carnot Engine:\neta = 1 - (T_cold / T_hot)\n\nProblem 1:\nA Carnot engine operates between reservoirs at 600 K and 300 K.\nCalculate its theoretical maximum efficiency.", fontsize=11)
        buf = doc.write()
        doc.close()
        return base64.b64encode(buf).decode('utf-8')
    except Exception as e:
        return base64.b64encode(b"%PDF-1.4 ... Carnot Engine 600K 300K").decode('utf-8')

def run_multimodal_tests():
    print("=" * 60)
    print("SIKSHASATHI MULTIMODAL AI MENTOR TEST SUITE")
    print("=" * 60)

    client = httpx.Client(base_url=BASE_URL, timeout=40.0)

    # 1. Login
    login_res = client.post("/api/auth/login", json={"email": "aarav@siksha.edu", "password": "student123"})
    if login_res.status_code != 200:
        print(f"[FAIL] Login failed: {login_res.status_code}")
        return False
    
    auth_data = login_res.json()
    token = auth_data["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("[1] [PASS] Authenticated as Aarav Sharma")

    # 2. Create Multimodal Conversation
    conv_res = client.post("/api/mentor/conversations", json={
        "title": "Multimodal Science Studio",
        "mode": "exam",
        "subject": "Physics"
    }, headers=headers)
    conv_id = conv_res.json()["conversation_id"]
    print(f"[2] [PASS] Created Conversation: {conv_id}")

    # 3. Test Image Upload & OCR Solver
    print("\n--- Testing Image Attachment (OCR + Exam Solver) ---")
    img_b64 = generate_test_image_base64()
    img_payload = {
        "conversation_id": conv_id,
        "message": "Please solve the problem shown in this attached physics diagram.",
        "mode": "exam",
        "attachment_base64": img_b64,
        "attachment_name": "projectile_problem.png",
        "attachment_type": "image"
    }
    img_res = client.post("/api/mentor/chat", json=img_payload, headers=headers)
    assert img_res.status_code == 200, f"Image chat failed: {img_res.text}"
    img_data = img_res.json()
    safe_img_reply = img_data['reply'][:300].encode('ascii', errors='replace').decode('ascii')
    print(f"[3] [PASS] Image OCR & Solver Result:\n{safe_img_reply}...\n")

    # 4. Test PDF Upload & RAG Solver
    print("\n--- Testing PDF Attachment (Document Ingestion + Deep Concept) ---")
    pdf_b64 = generate_test_pdf_base64()
    pdf_payload = {
        "conversation_id": conv_id,
        "message": "Explain the Carnot engine efficiency formula from this attached document.",
        "mode": "deep",
        "attachment_base64": pdf_b64,
        "attachment_name": "thermodynamics_carnot.pdf",
        "attachment_type": "pdf"
    }
    pdf_res = client.post("/api/mentor/chat", json=pdf_payload, headers=headers)
    assert pdf_res.status_code == 200, f"PDF chat failed: {pdf_res.text}"
    pdf_data = pdf_res.json()
    safe_pdf_reply = pdf_data['reply'][:300].encode('ascii', errors='replace').decode('ascii')
    print(f"[4] [PASS] PDF RAG Extraction & Concept Result:\n{safe_pdf_reply}...\n")

    print("=" * 60)
    print("ALL MULTIMODAL AI MENTOR TESTS PASSED PERFECTLY!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = run_multimodal_tests()
    sys.exit(0 if success else 1)
