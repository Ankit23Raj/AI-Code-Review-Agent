from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag.indexer import index_repository
from app.rag.search import search_similar_code

# build index first
index_repository("tests/fixtures")

sample_fact = {
    "file_path": "tests/fixtures/sql_injection.py",
    "symbol_name": "get_user",
    "snippet": 'query = "SELECT * FROM users WHERE id = " + user_id'
}

result = search_similar_code(sample_fact)

print(result)