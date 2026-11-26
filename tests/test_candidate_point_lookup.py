import pytest

from scrydb import Index


@pytest.mark.parametrize("precision", ["float", "int8", "binary"])
def test_lexical_rerank_scores_only_matching_candidates(precision):
    query = [1.0, .01, .01, .01, .01, .01, .01, .01]
    with Index.open(":memory:") as index:
        index.index_documents([
            {"id": "excluded", "text": "moon", "emb": query},
            {"id": "close", "text": "sun", "emb": [1, -.01, .01, .01, .01, .01, .01, .01]},
            {"id": "far", "text": "sun", "emb": [-x for x in query]},
            {"id": "missing-vector", "text": "sun"},
        ], store_int8_embeddings=True)
        index.index_queries([{"id": "q", "text": "sun", "emb": query}], store_int8_embeddings=True)
        statements = []
        index.conn.set_trace_callback(statements.append)
        results = index.batch_search("q", mode="lexical", rerank=precision)["q"]
        assert [hit.id for hit in results] == ["close", "far"]
        assert not any("embedding MATCH" in sql for sql in statements)
