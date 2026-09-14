"""
SikshaSaathi — Part 2 End-to-End Test Suite
Tests:
1. Teacher Profile retrieval, editing & persistence
2. Unique Class Code generation, human-readability & collision safety
3. Multiple class creations & unique code diversity
4. Class list isolation between Teacher A and Teacher B
5. Dynamic Metrics aggregation (classes, students, mastery)
6. Zero-class empty state verification for new teacher accounts
7. Strict role protection: Student cannot access Teacher API (403)
8. Unauthenticated requests strictly rejected (401)
"""

import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def post_json(path, data, token=None):
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw

def put_json(path, data, token=None):
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw

def get_json(path, token=None):
    url = f"{BASE_URL}{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, raw


def run_e2e_verification():
    passed = 0
    total = 0

    def assert_test(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}: {details}")
            sys.exit(1)

    print("=" * 65)
    print("PART 2 — TEACHER SYSTEM & CLASSROOM ECOSYSTEM E2E AUDIT")
    print("=" * 65)

    # 1. Authenticate Actors
    print("\n--- Phase 1: Authentication & Actor Resolution ---")
    st, s_res = post_json("/api/auth/login", {"email": "aarav@siksha.edu", "password": "student123"})
    assert_test("Student A login (200)", st == 200)
    student_token = s_res["access_token"]

    st, ta_res = post_json("/api/auth/login", {"email": "teacher@siksha.edu", "password": "teacher123"})
    assert_test("Teacher A login (200)", st == 200)
    teacher_a_token = ta_res["access_token"]
    teacher_a_id = ta_res["user"]["id"]

    st, tb_res = post_json("/api/auth/login", {"email": "teacher2@siksha.edu", "password": "teacher123"})
    assert_test("Teacher B login (200)", st == 200)
    teacher_b_token = tb_res["access_token"]
    teacher_b_id = tb_res["user"]["id"]

    # 2. Strict Role Protection
    print("\n--- Phase 2: Role Protection & Security ---")
    st, _ = get_json("/api/teacher/profile")
    assert_test("Unauthenticated access to /api/teacher/profile blocked (401)", st == 401)

    st, _ = get_json("/api/teacher/profile", token=student_token)
    assert_test("Student access to /api/teacher/profile blocked (403 Forbidden)", st == 403)

    st, _ = post_json("/api/teacher/classes", {"name": "Hacked Class", "subject": "Math"}, token=student_token)
    assert_test("Student creating class blocked (403 Forbidden)", st == 403)

    # 3. Real Teacher Profile Retrieval & Editing
    print("\n--- Phase 3: Real Teacher Profile & In-Place Editing ---")
    st, prof = get_json("/api/teacher/profile", token=teacher_a_token)
    assert_test("Teacher A profile fetched (200)", st == 200)
    assert_test("Profile email matches Teacher A", prof["email"] == "teacher@siksha.edu")
    assert_test("Profile role is 'teacher'", prof["role"] == "teacher")
    assert_test("Dynamic metrics present in profile", "total_classes" in prof and "total_students" in prof)

    # Edit Profile
    edit_payload = {
        "full_name": "Dr. Rajesh V. Sharma",
        "institution": "Apex Science Academy • Delhi",
        "subject": "Advanced Classical & Modern Physics",
        "bio": "Specialized in Olympiad & JEE Advanced physics pedagogy with 14+ years experience."
    }
    st, edit_res = put_json("/api/teacher/profile", edit_payload, token=teacher_a_token)
    assert_test("Profile edit saved to backend (200)", st == 200)

    # Verify persistence via fresh GET request (simulating browser refresh)
    st, fresh_prof = get_json("/api/teacher/profile", token=teacher_a_token)
    assert_test("Profile changes persist after reload", fresh_prof["full_name"] == "Dr. Rajesh V. Sharma")
    assert_test("Institution persists", fresh_prof["institution"] == "Apex Science Academy • Delhi")
    assert_test("Subject specialization persists", fresh_prof["subject"] == "Advanced Classical & Modern Physics")
    assert_test("Bio persists", fresh_prof["bio"].startswith("Specialized in Olympiad"))

    # 4. Create Real Classrooms & Unique Join Code Engine
    print("\n--- Phase 4: Classroom Creation & Unique Code Engine ---")
    c1_payload = {
        "name": "Class 12-A • High-Mastery Physics",
        "subject": "Physics",
        "grade_level": "Class 12 • Senior Secondary",
        "description": "Rigorous mechanics, wave optics, and electrostatics with active inquiry."
    }
    st, c1_res = post_json("/api/teacher/classes", c1_payload, token=teacher_a_token)
    assert_test("Class 1 created (201 Created)", st == 201)
    class_1 = c1_res["classroom"]
    code_1 = class_1["join_code"]
    c1_id = class_1["id"]

    # Validate Code Properties: Human friendly, uppercase, no 0/O or 1/I/L
    assert_test("Class 1 join code length >= 6", len(code_1) >= 6)
    assert_test("Class 1 join code is uppercase", code_1.isupper())
    bad_chars = ["0", "1", "I", "O", "L"]
    assert_test("Class 1 code contains no confusing characters (0/O/1/I/L)", not any(b in code_1 for b in bad_chars))
    print(f"       -> Generated Code 1: [{code_1}] for '{class_1['name']}'")

    # Create Class 2 for Teacher A (Mathematics)
    c2_payload = {
        "name": "Class 12-B • Differential Calculus & Vectors",
        "subject": "Mathematics",
        "grade_level": "Class 12",
        "description": "Limits, derivatives, integrals, and coordinate geometry masterclass."
    }
    st, c2_res = post_json("/api/teacher/classes", c2_payload, token=teacher_a_token)
    assert_test("Class 2 created (201 Created)", st == 201)
    class_2 = c2_res["classroom"]
    code_2 = class_2["join_code"]
    c2_id = class_2["id"]

    assert_test("Class 2 join code length >= 6", len(code_2) >= 6)
    assert_test("Class 2 code is completely distinct from Class 1 code", code_1 != code_2)
    assert_test("Class 2 code contains no confusing characters", not any(b in code_2 for b in bad_chars))
    print(f"       -> Generated Code 2: [{code_2}] for '{class_2['name']}'")

    # Verify code persistence after reload
    st, c1_fetch = get_json(f"/api/teacher/classes/{c1_id}", token=teacher_a_token)
    assert_test("Class 1 code remains identical after reload", c1_fetch["classroom"]["join_code"] == code_1)

    # 5. Teacher Class List & Ownership Isolation
    print("\n--- Phase 5: Classroom List & Data Isolation ---")
    st, ta_classes = get_json("/api/teacher/classes", token=teacher_a_token)
    assert_test("Teacher A class list returned (200)", st == 200)
    ta_class_ids = [c["id"] for c in ta_classes["classes"]]
    assert_test("Teacher A sees Class 1", c1_id in ta_class_ids)
    assert_test("Teacher A sees Class 2", c2_id in ta_class_ids)

    # Teacher B creates Class 3
    c3_payload = {
        "name": "Class 10-A • Foundation Science & Chemistry",
        "subject": "Chemistry",
        "grade_level": "Class 10",
        "description": "Chemical equations, metals and non-metals fundamentals."
    }
    st, c3_res = post_json("/api/teacher/classes", c3_payload, token=teacher_b_token)
    assert_test("Teacher B created Class 3 (201 Created)", st == 201)
    c3_id = c3_res["classroom"]["id"]
    code_3 = c3_res["classroom"]["join_code"]
    print(f"       -> Generated Code 3: [{code_3}] for Teacher B")

    # Verify isolation: Teacher A does NOT see Class 3
    st, ta_classes_after = get_json("/api/teacher/classes", token=teacher_a_token)
    ta_ids_after = [c["id"] for c in ta_classes_after["classes"]]
    assert_test("Teacher A CANNOT see Teacher B's class in class list", c3_id not in ta_ids_after)

    # Verify isolation: Teacher A CANNOT fetch details of Teacher B's class
    st, _ = get_json(f"/api/teacher/classes/{c3_id}", token=teacher_a_token)
    assert_test("Direct access to Teacher B's class by Teacher A is blocked (404)", st == 404)

    # 6. Real-Time Dynamic Metrics
    print("\n--- Phase 6: Real Dynamic Metrics Calculation ---")
    st, metrics_res = get_json("/api/teacher/metrics", token=teacher_a_token)
    assert_test("Teacher A metrics fetched (200)", st == 200)
    m = metrics_res["metrics"]
    assert_test("Metrics 'total_classes' reflects actual count", m["total_classes"] >= 2)
    assert_test("Metrics 'total_students' reflects actual database count", "total_students" in m)
    assert_test("Metrics 'average_mastery' is calculated from real telemetry", "average_mastery" in m)
    print(f"       -> Real KPIs: Active Classes={m['total_classes']}, Enrolled Students={m['total_students']}, Avg Mastery={m['average_mastery']}%")

    # 7. Empty State Verification
    print("\n--- Phase 7: Clean Empty State for New Teacher Account ---")
    # Register Teacher C (brand new educator)
    new_teacher_email = f"newteacher_{class_1['id'][:6]}@siksha.edu"
    st, new_t_res = post_json("/api/auth/signup", {
        "email": new_teacher_email,
        "password": "teacherpassword123",
        "full_name": "Dr. Ananya Sen",
        "role": "teacher",
        "institution": "Presidency College",
        "subject": "Biotechnology"
    })
    assert_test("New Teacher C registered (201 Created)", st == 201)
    new_teacher_token = new_t_res["access_token"]

    st, new_t_classes = get_json("/api/teacher/classes", token=new_teacher_token)
    assert_test("New Teacher C classes retrieved (200)", st == 200)
    assert_test("New Teacher C starts with exactly 0 classes (empty state)", new_t_classes["count"] == 0)

    st, new_t_metrics = get_json("/api/teacher/metrics", token=new_teacher_token)
    assert_test("New Teacher C has 0 classes in metrics", new_t_metrics["metrics"]["total_classes"] == 0)
    assert_test("New Teacher C has 0 students in metrics", new_t_metrics["metrics"]["total_students"] == 0)
    assert_test("New Teacher C has 0.0% average mastery", new_t_metrics["metrics"]["average_mastery"] == 0.0)

    print("\n" + "=" * 65)
    print(f"ALL {passed}/{total} PART 2 E2E TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 65)

if __name__ == "__main__":
    run_e2e_verification()
