import json
import os

REGISTRY_FILE = "document_registry.json"


def _load_registry() -> dict:
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_registry(registry: dict):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def add_document(filename: str, chunks_created: int):
    """Register a newly ingested document."""
    registry = _load_registry()
    registry[filename] = {
        "chunks_created": chunks_created
    }
    _save_registry(registry)


def remove_document(filename: str):
    """Remove a document from the registry."""
    registry = _load_registry()
    if filename in registry:
        del registry[filename]
        _save_registry(registry)


def list_documents() -> list[dict]:
    """Return list of all registered documents."""
    registry = _load_registry()
    return [
        {"filename": name, "chunks_created": info["chunks_created"]}
        for name, info in registry.items()
    ]