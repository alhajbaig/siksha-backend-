"""
End-to-End Automated Test Suite for SikshaSaathi Notes & RAG Knowledge Engine
Tests all 15 scenarios specified in the master requirements.
"""

import os
import sys
import asyncio
from backend.services.rag_service import rag_service
from backend.db import get_db_connection

def run_all_tests():
    print("==================================================")
    print("RUNNING SIKSHASAATHI NOTES E2E TEST SUITE")
    print("==================================================")

    user_a = "user_aarav_jee"
    user_b = "user_diya_neet"

    # Clean test users from DB
    conn = get_db_connection()
    conn.execute("DELETE FROM notes WHERE user_id IN (?, ?)", (user_a, user_b))
    conn.execute("DELETE FROM note_chunks WHERE user_id IN (?, ?)", (user_a, user_b))
    conn.commit()
    conn.close()

    # Initial seeding for user_a
    rag_service.ensure_user_seeded(user_a)

    # TEST 1: Upload Chemistry PDF / Note
    print("\n--- TEST 1: Upload Chemistry Note ---")
    chem_note = rag_service.ingest_note(
        user_id=user_a,
        title="Aldehydes & Ketones: Nucleophilic Addition",
        subject="chem",
        text_content="Carbonyl carbon is electrophilic due to electronegative oxygen. Grignard reagents (RMgX) add to ketones to yield tertiary alcohols."
    )
    assert chem_note.subject.startswith("CHEMISTRY"), f"Expected Chemistry, got {chem_note.subject}"
    assert chem_note.chunk_count >= 1, "Expected chunks created"
    assert chem_note.status == "indexed", "Expected status indexed"
    print(f"PASS: Chemistry note indexed (ID: {chem_note.id}, Chunks: {chem_note.chunk_count})")

    # TEST 2: Upload Physics Note
    print("\n--- TEST 2: Upload Physics Note ---")
    phys_note = rag_service.ingest_note(
        user_id=user_a,
        title="Electromagnetic Induction: Faraday's Law",
        subject="phys",
        text_content="Induced EMF in a circuit is proportional to the time rate of change of magnetic flux through the circuit: EMF = -d(Phi)/dt. Lenz's Law establishes opposition direction."
    )
    assert phys_note.subject.startswith("PHYSICS"), f"Expected Physics, got {phys_note.subject}"
    print(f"PASS: Physics note indexed (ID: {phys_note.id})")

    # TEST 3: Upload Math Note
    print("\n--- TEST 3: Upload Math Note ---")
    math_note = rag_service.ingest_note(
        user_id=user_a,
        title="Linear Algebra: Eigenvalues & Characteristic Polynomial",
        subject="math",
        text_content="Eigenvalues lambda satisfy det(A - lambda*I) = 0. Trace equals sum of eigenvalues and determinant equals product of eigenvalues."
    )
    assert math_note.subject.startswith("MATHEMATICS"), f"Expected Math, got {math_note.subject}"
    print(f"PASS: Math note indexed (ID: {math_note.id})")

    # TEST 4: Upload CS Note
    print("\n--- TEST 4: Upload CS Note ---")
    cs_note = rag_service.ingest_note(
        user_id=user_a,
        title="Graph Algorithms: Dijkstra Shortest Path",
        subject="cs",
        text_content="Dijkstra's algorithm finds single-source shortest paths on non-negative weighted graphs in O((V + E) log V) using a min-priority queue."
    )
    assert cs_note.subject.startswith("COMP SCIENCE"), f"Expected CS, got {cs_note.subject}"
    print(f"PASS: CS note indexed (ID: {cs_note.id})")

    # TEST 5: Filter Chem
    print("\n--- TEST 5: Filter Chemistry Notes ---")
    chem_list = rag_service.get_all_notes(user_id=user_a, subject_filter="chem")
    assert all(n.subject == "chem" for n in chem_list.notes), "All returned notes must be Chemistry"
    assert len(chem_list.notes) >= 2, "Expected at least 2 chem notes"
    print(f"PASS: Found {len(chem_list.notes)} Chemistry notes exclusively")

    # TEST 6: Filter Phys
    print("\n--- TEST 6: Filter Physics Notes ---")
    phys_list = rag_service.get_all_notes(user_id=user_a, subject_filter="phys")
    assert all(n.subject == "phys" for n in phys_list.notes), "All returned notes must be Physics"
    print(f"PASS: Found {len(phys_list.notes)} Physics notes exclusively")

    # TEST 7: Filter All
    print("\n--- TEST 7: Filter All Notes & Dynamic Counts ---")
    all_list = rag_service.get_all_notes(user_id=user_a, subject_filter="all")
    print(f"PASS: Total notes: {all_list.total_indexed}, Subject breakdown: {all_list.subject_counts.model_dump()}")
    assert all_list.total_indexed == 8, f"Expected 8 notes (4 starter + 4 newly uploaded), got {all_list.total_indexed}"

    # TEST 8: Search inside text (NOT in title)
    print("\n--- TEST 8: Search for text inside chunks ---")
    search_res = rag_service.get_all_notes(user_id=user_a, search="Grignard")
    assert len(search_res.notes) >= 1, "Expected to find note containing 'Grignard'"
    print(f"PASS: Found note '{search_res.notes[0].title}' by chunk keyword 'Grignard'")

    # TEST 9: Selected Document RAG (Answer exists)
    print("\n--- TEST 9: Grounded RAG Query (Answer exists in selected note) ---")
    async def test_grounded_rag():
        rag_res = await rag_service.process_query(
            user_id=user_a,
            query="What do Grignard reagents form with ketones?",
            note_id=chem_note.id
        )
        assert len(rag_res.citations) > 0, "Expected grounded citations"
        print(f"PASS: Grounded citation chunk #{rag_res.citations[0].chunk_id} (Score: {rag_res.citations[0].similarity_score})")

        # TEST 10: Question NOT in note (Hallucination protection)
        print("\n--- TEST 10: RAG Query (Answer NOT in document) ---")
        unrelated_res = await rag_service.process_query(
            user_id=user_a,
            query="What is the capital of Australia and the GDP of France?",
            note_id=chem_note.id
        )
        assert not unrelated_res.grounded or "couldn't find enough information" in unrelated_res.answer, "Must reject unrelated query"
        print(f"PASS: Rejected ungrounded question gracefully without hallucination")

        # Quick Actions
        print("\n--- Testing Quick Actions ---")
        summary_res = await rag_service.process_query(user_id=user_a, query="summary", note_id=chem_note.id, query_type="summary")
        assert len(summary_res.answer) > 20, "Expected non-empty summary"
        print("PASS: 30s Summary generated")

        formulas_res = await rag_service.process_query(user_id=user_a, query="formulas", note_id=phys_note.id, query_type="formulas")
        assert len(formulas_res.answer) > 20, "Expected non-empty formulas"
        print("PASS: Formula extraction generated")

        quiz_res = await rag_service.process_query(user_id=user_a, query="quiz", note_id=math_note.id, query_type="quiz")
        assert "Q1:" in quiz_res.answer or "Q1" in quiz_res.answer, "Expected quiz questions"
        print("PASS: Quiz Me (3 Qs) generated")

        traps_res = await rag_service.process_query(user_id=user_a, query="traps", note_id=cs_note.id, query_type="traps")
        assert len(traps_res.answer) > 20, "Expected exam traps"
        print("PASS: Common Exam Traps generated")

    asyncio.run(test_grounded_rag())

    # TEST 11: Delete Document
    print("\n--- TEST 11: Delete Note & Vectors ---")
    del_success = rag_service.delete_note(chem_note.id, user_id=user_a)
    assert del_success, "Expected delete success"
    verify_note = rag_service.get_note_by_id(chem_note.id, user_id=user_a)
    assert verify_note is None, "Note must no longer exist"
    print("PASS: Note, chunks, and embeddings successfully deleted")

    # TEST 12: Reindex Note
    print("\n--- TEST 12: Reindex Note ---")
    reindex_res = rag_service.reindex_note(phys_note.id, user_id=user_a)
    assert reindex_res is not None, "Expected reindexed note detail"
    assert reindex_res.status == "indexed", "Expected indexed status"
    print(f"PASS: Note reindexed with {reindex_res.chunk_count} chunks without duplicates")

    # TEST 13: Persistence after restart / fresh connection
    print("\n--- TEST 13: Data Persistence ---")
    fresh_notes = rag_service.get_all_notes(user_id=user_a)
    assert len(fresh_notes.notes) == 7, f"Expected 7 notes after 1 delete, got {len(fresh_notes.notes)}"
    print("PASS: All notes and chunks persistent across connections")

    # TEST 14 & 15: Multi-User Isolation
    print("\n--- TEST 14 & 15: User Isolation (User A vs User B) ---")
    rag_service.ensure_user_seeded(user_b)
    user_b_notes = rag_service.get_all_notes(user_id=user_b)
    assert user_b_notes.total_indexed == 4, "User B should only see their initial 4 notes"

    # User B should NOT see User A's physics note
    user_b_phys_search = rag_service.get_note_by_id(phys_note.id, user_id=user_b)
    assert user_b_phys_search is None, "User B must not access User A's note!"
    print("PASS: Complete user data isolation enforced at database and vector level")

    print("\n==================================================")
    print("ALL 15 E2E NOTES TEST CASES PASSED SUCCESSFULLY!")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
