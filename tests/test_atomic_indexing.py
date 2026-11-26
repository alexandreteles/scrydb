import sqlite3

import pytest

from scrydb import Index


def test_last_duplicate_wins_and_upsert_removes_obsolete_vectors():
    with Index.open(":memory:") as index:
        docs = [
            {"id": "a", "text": "old", "emb": [1.] * 8},
            {"id": "a", "text": "new", "emb": [-1.] * 8},
        ]
        index.index_documents(docs, store_int8_embeddings=True)
        assert [h.id for h in index.search("new")] == ["a"]
        assert not index.search("old")
        index.index_documents([docs[0]], store_full_embeddings=False)
        assert "a" in index.document_embeddings_binary
        assert "a" not in index.document_embeddings_int8
        assert "a" not in index.document_embeddings
        index.index_documents([{"id": "a", "text": "words"}])
        assert "a" not in index.document_embeddings_binary


def test_vector_failure_rolls_back_every_representation_in_the_batch():
    with Index.open(":memory:") as index:
        index.index_documents([{"id": "a", "text": "original", "emb": [1.] * 8}])
        with pytest.raises(sqlite3.DatabaseError):
            index.index_documents([
                {"id": "a", "text": "replacement", "emb": [-1.] * 8},
                {"id": "b", "text": "invalid", "emb": [-1.] * 16},
            ])
        assert list(index.documents) == ["a"]
        assert [h.id for h in index.search("original")] == ["a"]
        assert not index.search("replacement")
        assert index.document_embeddings["a"].tolist() == [1.] * 8
