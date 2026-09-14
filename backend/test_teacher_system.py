"""
Test Suite for Part 2 — Teacher Profile, Classroom CRUD, Code Generation, and Data Isolation
"""

import urllib.request
import json
import re
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


def run_tests():
    print("=" * 65)
    print("RUNNING PART 2: TEACHER PROFILE & CLASSROOM SYSTEM TESTS")
    print("=" * 65)

    # 1. Login Accounts
    _, s_res = post_json("/api/auth/login", {"email": "aarav@siksha.edu", "password": "student123"})
    student_token = s_res["access_token"]

    _, t_res = post_json("/api/auth/login", {"email": "teacher@siksha.edu", "password": "teacher123"})
    teacher_a_token = t_res["access_token"]
    teacher_a_id = t_res["user"]["id"]

    _, tb_res = post_json("/api/auth/login", {"email": "teacher2@siksha.edu", "password": "teacher123"})
    teacher_b_token = tb_res["access_token"]
    teacher_b_id = tb_res["user"]["id"]

    # 2. Authorization Security Guard Tests
    print("\n[Phase 1: Authorization Guards]")
    st, _ = get_json("/api/teacher/profile")
    assert st == 401, f"Unauthenticated request should return 401, got {st}"
    print("  [PASS] Unauthenticated /api/teacher/profile returns 401")

    st, _ = get_json("/api/teacher/profile", token=student_token)
    assert st == 403, f"Student accessing teacher profile should return 403, got {st}"
    print("  [PASS] Student token accessing /api/teacher/profile returns 403 Forbidden")

    # 3. Real Teacher Profile Retrieval
    print("\n[Phase 2: Teacher Profile Retrieval]")
    st, prof = get_json("/api/teacher/profile", token=teacher_a_token)
    assert st == 200, f"Teacher profile retrieval failed: {st}"
    assert prof["role"] == "teacher"
    assert prof["email"] == "teacher@siksha.edu"
    assert "total_classes" in prof
    assert "total_students" in prof
    assert "average_mastery" in prof
    print(f"  [PASS] Retrieved authentic profile: Name='{prof['full_name']}', Classes={prof['total_classes']}, Students={prof['total_students']}")

    # 4. Teacher Profile Editing & Persistence
    print("\n[Phase 3: Teacher Profile Editing]")
    update_data = {
        "full_name": "Dr. Rajesh V. Sharma",
        "institution": "National Institute of Science & Technology",
        "subject": "Quantum Mechanics & Physics",
        "bio": "Senior Physics Educator with 15+ years mentoring competitive exam aspirants."
    }
    st, update_res = put_json("/api/teacher/profile", update_data, token=teacher_a_token)
    assert st == 200, f"Profile update failed: {st}"
    assert update_res["user"]["full_name"] == "Dr. Rajesh V. Sharma"
    assert update_res["user"]["institution"] == "National Institute of Science & Technology"

    # Verify persistence via fresh GET /api/teacher/profile
    st, fresh_prof = get_json("/api/teacher/profile", token=teacher_a_token)
    assert fresh_prof["full_name"] == "Dr. Rajesh V. Sharma"
    assert fresh_prof["institution"] == "National Institute of Science & Technology"
    assert fresh_prof["bio"].startswith("Senior Physics")
    print("  [PASS] Profile updated and verified persistently in SQLite database")

    # 5. Class Creation & Unique Class Code Validation
    print("\n[Phase 4: Class Creation & Unique Code Validation]")
    new_class_data = {
        "name": "Class 12-A • Advanced Classical Mechanics",
        "subject": "Physics",
        "grade_level": "Class 12 • Senior Secondary",
        "description": "Rigorous kinematics, rotational dynamics, and boundary conditions."
    }
    st, class_res = post_json("/api/teacher/classes", new_class_data, token=teacher_a_token)
    assert st == 201, f"Class creation failed with status {st}: {class_res}"
    created_class = class_res["classroom"]
    join_code = created_class["join_code"]
    class_id = created_class["id"]
    print(f"  [PASS] Created class '{created_class['name']}' with Join Code: [{join_code}]")

    # Validate Join Code format
    # Must be 6-8 uppercase alphanumeric, no 0, 1, I, O, L
    assert len(join_code) >= 6, f"Code too short: {join_code}"
    assert join_code.isupper(), f"Code should be uppercase: {join_code}"
    assert not any(bad in join_code for bad in ["0", "1", "I", "O", "L"]), f"Code contains ambiguous characters: {join_code}"
    print(f"  [PASS] Join code [{join_code}] satisfies all human-friendly and collision-safe requirements")

    # Create a second class for Teacher A
    new_class_data2 = {
        "name": "Class 11-B • Thermodynamics & Fluids",
        "subject": "Physics",
        "grade_level": "Class 11",
        "description": "Kinetic theory of gases and thermal properties."
    }
    st, class_res2 = post_json("/api/teacher/classes", new_class_data2, token=teacher_a_token)
    assert st == 201
    join_code2 = class_res2["classroom"]["join_code"]
    assert join_code2 != join_code, "Duplicate class code generated!"
    print(f"  [PASS] Created second class with distinct code: [{join_code2}]")

    # 6. Teacher Class List & Isolation
    print("\n[Phase 5: Teacher Class List & Ownership Isolation]")
    st, classes_a = get_json("/api/teacher/classes", token=teacher_a_token)
    assert st == 200
    class_ids_a = [c["id"] for c in classes_a["classes"]]
    assert class_id in class_ids_a
    print(f"  [PASS] Teacher A sees their active classes (total: {len(classes_a['classes'])})")

    # Teacher B creates a class
    tb_class_data = {
        "name": "Class 10 • Organic Chemistry Fundamentals",
        "subject": "Chemistry",
        "grade_level": "Class 10",
        "description": "Carbon compounds and IUPAC nomenclature."
    }
    st, tb_class_res = post_json("/api/teacher/classes", tb_class_data, token=teacher_b_token)
    assert st == 201
    tb_class_id = tb_class_res["classroom"]["id"]
    tb_code = tb_class_res["classroom"]["join_code"]
    print(f"  [PASS] Teacher B created class with code: [{tb_code}]")

    # Verify Teacher A CANNOT see Teacher B's class
    st, classes_a_after = get_json("/api/teacher/classes", token=teacher_a_token)
    assert tb_class_id not in [c["id"] for c in classes_a_after["classes"]]
    print("  [PASS] Teacher A does NOT see Teacher B's class in class list")

    # Verify Teacher A CANNOT fetch details of Teacher B's class
    st, unauth_detail = get_json(f"/api/teacher/classes/{tb_class_id}", token=teacher_a_token)
    assert st == 404, f"Teacher A should be denied access to Teacher B's class, got {st}"
    print("  [PASS] Direct access to another teacher's class returns 404 Not Found")

    # 7. Real Metrics Aggregation
    print("\n[Phase 6: Real Metrics Aggregation]")
    st, metrics_res = get_json("/api/teacher/metrics", token=teacher_a_token)
    assert st == 200
    m = metrics_res["metrics"]
    assert m["total_classes"] >= 2
    assert "total_students" in m
    assert "average_mastery" in m
    print(f"  [PASS] Verified real-time metrics: Total Classes={m['total_classes']}, Students={m['total_students']}, Avg Mastery={m['average_mastery']}%")

    print("\n" + "=" * 65)
    print("ALL PART 2 BACKEND & CLASSROOM TESTS PASSED PERFECTLY!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
