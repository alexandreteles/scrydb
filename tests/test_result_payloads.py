from scrydb import Index


def test_bulk_payload_reads_preserve_ranking_and_skip_absent_ids():
    with Index.open(":memory:", vec_ext_path=None) as index:
        index.index_documents([{"id": str(i), "text": "words"} for i in range(15)])
        ranked = [(str(i), {"score": i}) for i in range(16, -1, -1)]
        queries = []
        index.conn.set_trace_callback(queries.append)
        hits = index._materialize(ranked, len(ranked))
        assert [hit.id for hit in hits] == [str(i) for i in range(14, -1, -1)]
        assert all(hit.document["id"] == hit.id and hit.score == int(hit.id) for hit in hits)
        assert len([sql for sql in queries if "FROM documents " in sql]) == 1
