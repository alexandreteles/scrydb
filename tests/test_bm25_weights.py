import pytest

from scrydb import Index


def test_text_weight_matches_fts5_and_preserves_the_legacy_alias():
    with Index.open(":memory:", vec_ext_path=None) as index:
        index.index_documents([{"id": "d", "text": "green green"}])
        index.index_queries([{"id": "q", "text": "green"}])
        expected = -index.conn.execute(
            "SELECT bm25(documents_fts, 0, 2.5) FROM documents_fts WHERE documents_fts MATCH 'green'"
        ).fetchone()[0]
        assert index.search("green", bm25_text_weight=2.5)[0].score == expected
        with pytest.warns(DeprecationWarning):
            assert index.batch_search("q", bm25_b=0.2, bm25_k1=2.5)["q"][0].score == expected
