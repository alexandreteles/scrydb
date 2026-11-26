from scrydb import Index


def test_equal_fusion_scores_break_ties_by_document_id():
    with Index.open(":memory:", vec_ext_path=None) as index:
        lexical = [("d2", {}), ("d1", {}), ("z", {})]
        dense = [("d1", {}), ("d2", {}), ("a", {})]
        hits = index._reciprocal_rank_fusion(lexical, dense, 60)
        assert [doc_id for doc_id, _ in hits] == ["d1", "d2", "a", "z"]
