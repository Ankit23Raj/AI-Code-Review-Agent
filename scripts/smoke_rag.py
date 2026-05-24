from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag.indexer import index_repository

result = index_repository("tests/fixtures")

print(result)