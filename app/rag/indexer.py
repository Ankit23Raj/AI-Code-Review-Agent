from pathlib import Path

from app.rag.embeddings import create_embeddings

INDEX = []


def index_repository(repo_path):
    """
    Temporary starter repository indexer.

    Later this function will:
    - scan repository files
    - parse code
    - generate embeddings
    - store vectors in a vector database
    """

    print(f"Indexing repository: {repo_path}")

    INDEX.clear()
    repo_path_obj = Path(repo_path)
    for path in sorted(repo_path_obj.rglob("*.py")):
        content = path.read_text(encoding="utf-8")
        embedding = create_embeddings(content)

        INDEX.append({
            "file_path": str(path),
            "content": content,
            "embedding": embedding.get("embedding", [])
        })

    return {
        "repo_path": repo_path,
        "indexed_files": len(INDEX),
        "index": INDEX
    }
