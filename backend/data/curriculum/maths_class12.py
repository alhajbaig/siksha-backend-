"""
SIKSHA SAATHI — Mathematics Curriculum: NCERT Class 12 (Complete 13 Chapters)
13 Distinct Topic Modules with Dedicated Detailed Notes, Revision Sheets,
Active-Recall Flashcards, Interactive Flowcharts, Zoomable Mind Maps, and RAG Chunks.
Fully aligned with NCERT Mathematics Class XII Textbooks (Parts 1 and 2, Chapters 1 to 13).
"""

import os
import json
from typing import Dict, List, Any

ENHANCED_DATA_PATH = os.path.join(os.path.dirname(__file__), "maths_class12_enhanced.json")

def get_all_maths_topics() -> List[Dict[str, Any]]:
    """Returns the complete array of 13 structured Mathematics Class 12 topic modules."""
    if os.path.exists(ENHANCED_DATA_PATH):
        try:
            with open(ENHANCED_DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load enhanced mathematics JSON: {e}")
    return []
