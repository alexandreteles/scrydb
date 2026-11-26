import pytest

from scrydb import Index


@pytest.mark.parametrize("options", [
    {"mode": "semantic", "precision": "int8"},
    {"mode": "hybrid", "precision": "int8"},
    {"mode": "lexical", "rerank": "int8"},
])
def test_missing_dense_stage_is_reported(options):
    with Index.open(":memory:") as index:
        index.index_documents([{"id": "d", "text": "term", "emb": [1] * 8}])
        index.index_queries([{"id": "q", "text": "term", "emb": [1] * 8}])
        with pytest.raises(RuntimeError, match="no int8 vector index"):
            index.batch_search("q", **options)


def test_empty_document_collection_has_no_hits():
    with Index.open(":memory:") as index:
        index.index_queries([{"id": "q", "emb": [1] * 8}])
        assert not index.batch_search("q", mode="semantic")["q"]
