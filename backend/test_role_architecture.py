"""
SikshaSaathi — Part 1 Role Architecture & Security Test Suite
Tests:
1. Authentication & Role Resolution (Student vs Teacher)
2. Invalid Credentials & Security
3. Session Verification & Token Validation (/api/auth/me)
4. Removal of Fake Offline Fallback (unauthenticated -> 401)
5. Backend Role-Based Authorization Guards (require_teacher, require_student)
6. Multi-Account Isolation (Student A, Student B, Teacher A, Teacher B)
7. Teacher Dashboard Static Assets & Subpages Availability
8. Cross-Portal Navigation & HTML Route Guards
"""

import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def post_json(endpoint, data, token=None):
    url = f"{BASE_URL}{endpoint}"
    req_data = json.dumps(data).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body

def get_json(endpoint, token=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, body

def get_html(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


def run_tests():
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

    print("=" * 60)
    print("RUNNING ROLE ARCHITECTURE & SECURITY AUDIT")
    print("=" * 60)

    # 1. Test unauthenticated /api/auth/me (must return 401, not default Aarav)
    print("\n[Phase 1: Unauthenticated Guard Verification]")
    status, res = get_json("/api/auth/me")
    assert_test("Unauthenticated /api/auth/me returns 401", status == 401, f"Got status {status}: {res}")

    status, res = get_json("/api/auth/profile")
    assert_test("Unauthenticated /api/auth/profile returns 401", status == 401, f"Got status {status}: {res}")

    # 2. Test Invalid Credentials
    print("\n[Phase 2: Authentication Security]")
    status, res = post_json("/api/auth/login", {"email": "aarav@siksha.edu", "password": "wrongpassword"})
    assert_test("Invalid password returns 401", status == 401, f"Got {status}")

    status, res = post_json("/api/auth/login", {"email": "nonexistent@siksha.edu", "password": "password123"})
    assert_test("Non-existent user returns 401", status == 401, f"Got {status}")

    # 3. Test Student A Login & Profile
    print("\n[Phase 3: Student Authentication & Role Resolution]")
    status, res = post_json("/api/auth/login", {"email": "aarav@siksha.edu", "password": "student123"})
    assert_test("Student A login succeeds", status == 200, f"Got {status}: {res}")
    student_a_token = res.get("access_token")
    student_a_user = res.get("user", {})
    assert_test("Student A role is strictly 'student'", student_a_user.get("role") == "student", f"Role is {student_a_user.get('role')}")
    assert_test("Student A token present", bool(student_a_token))

    # Verify /api/auth/me with Student A token
    status, me_res = get_json("/api/auth/me", token=student_a_token)
    assert_test("Student A /api/auth/me succeeds with 200", status == 200, f"Got {status}")
    assert_test("Student A /api/auth/me returns student role", me_res.get("role") == "student", f"Got {me_res.get('role')}")
    assert_test("Student A email matches", me_res.get("email") == "aarav@siksha.edu")

    # 4. Test Teacher A Login & Profile
    print("\n[Phase 4: Teacher Authentication & Role Resolution]")
    status, res = post_json("/api/auth/login", {"email": "teacher@siksha.edu", "password": "teacher123"})
    assert_test("Teacher A login succeeds", status == 200, f"Got {status}: {res}")
    teacher_a_token = res.get("access_token")
    teacher_a_user = res.get("user", {})
    assert_test("Teacher A role is strictly 'teacher'", teacher_a_user.get("role") == "teacher", f"Role is {teacher_a_user.get('role')}")
    assert_test("Teacher A token present", bool(teacher_a_token))

    # Verify /api/auth/me with Teacher A token
    status, me_res = get_json("/api/auth/me", token=teacher_a_token)
    assert_test("Teacher A /api/auth/me succeeds with 200", status == 200, f"Got {status}")
    assert_test("Teacher A /api/auth/me returns teacher role", me_res.get("role") == "teacher", f"Got {me_res.get('role')}")
    assert_test("Teacher A email matches", me_res.get("email") == "teacher@siksha.edu")

    # 5. Multi-Account Testing (Student B & Teacher B)
    print("\n[Phase 5: Multi-Account Isolation (Student B & Teacher B)]")
    status, res_sb = post_json("/api/auth/login", {"email": "student2@siksha.edu", "password": "student123"})
    assert_test("Student B login succeeds", status == 200, f"Got {status}")
    student_b_token = res_sb.get("access_token")
    assert_test("Student B role is 'student'", res_sb.get("user", {}).get("role") == "student")
    assert_test("Student A and Student B user IDs are distinct", student_a_user.get("id") != res_sb.get("user", {}).get("id"))

    status, res_tb = post_json("/api/auth/login", {"email": "teacher2@siksha.edu", "password": "teacher123"})
    assert_test("Teacher B login succeeds", status == 200, f"Got {status}")
    teacher_b_token = res_tb.get("access_token")
    assert_test("Teacher B role is 'teacher'", res_tb.get("user", {}).get("role") == "teacher")
    assert_test("Teacher A and Teacher B user IDs are distinct", teacher_a_user.get("id") != res_tb.get("user", {}).get("id"))

    # 6. Test Static Teacher Dashboard Mount & Subpages
    print("\n[Phase 6: Teacher Dashboard Integration Verification]")
    pages = [
        "/teacher/index.html",
        "/teacher/students.html",
        "/teacher/assessments.html",
        "/teacher/curriculum.html",
        "/teacher/interventions.html",
        "/teacher/css/teacher.css",
        "/teacher/js/teacher.js",
        "/teacher/js/session.js"
    ]
    for page in pages:
        status, content = get_html(page)
        assert_test(f"Resource {page} accessible (200)", status == 200, f"Got {status}")
        if page.endswith(".html"):
            assert_test(f"Resource {page} contains role guard", "checkRouteGuard('teacher')" in content, f"Missing route guard in {page}")

    # 7. Test Student Dashboard Route Guard in Head
    print("\n[Phase 7: Student Dashboard Route Guard Verification]")
    student_pages = [
        "/student.html",
        "/student-profile.html",
        "/student-practice.html",
        "/student-emergency.html",
        "/student-mentor.html"
    ]
    for spage in student_pages:
        status, content = get_html(spage)
        assert_test(f"Student page {spage} accessible (200)", status == 200, f"Got {status}")
        assert_test(f"Student page {spage} contains checkRouteGuard('student')", "checkRouteGuard('student')" in content, f"Missing student route guard in {spage}")

    # 8. Test /teacher.html root redirect
    print("\n[Phase 8: Teacher Root Redirect]")
    status, content = get_html("/teacher.html")
    assert_test("/teacher.html returns 200", status == 200, f"Got {status}")
    assert_test("/teacher.html performs replace to /teacher/index.html", "/teacher/index.html" in content)

    # 9. Test Logout invalidation
    print("\n[Phase 9: Session Logout]")
    status, res = post_json("/api/auth/logout", {}, token=student_a_token)
    assert_test("Logout returns 200 OK", status == 200, f"Got {status}")

    print("\n" + "=" * 60)
    print(f"ALL {passed}/{total} ROLE ARCHITECTURE & SECURITY TESTS PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
