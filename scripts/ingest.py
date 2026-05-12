"""
CloverBot - Knowledge Base Ingestion Script
Run this after adding or updating files in the knowledge/ directory.

Usage:
    python scripts/ingest.py
"""

import sys
import os

# Add parent directory to path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag import ingest_knowledge_base

if __name__ == "__main__":
    print("CloverBot Knowledge Base Ingestion")
    print("=" * 40)
    count = ingest_knowledge_base()
    print(f"\nDone. Ingested {count} document(s).")
    print("The knowledge base is ready for CloverBot to use.")
