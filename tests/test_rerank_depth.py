import pytest

from scrydb import Index


@pytest.mark.parametrize("mode", ["semantic", "hybrid"])
def test_dense_rerank_can_promote_a_hit_below_the_output_limit(mode):
    with Index.open(":memory:") as index:
        query = [1, .01, .01, .01, .01, .01, .01, .01]
        index.index_documents([
            {"id": "same-sign", "text": "one", "emb": [.01, 1, .01, .01, .01, .01, .01, .01]},
            {"id": "closest", "text": "two", "emb": [1, -.01, .01, .01, .01, .01, .01, .01]},
        ])
        index.index_queries([{"id": "q", "text": "unmatched", "emb": query}])
        settings = dict(mode=mode, top_k=1, candidate_limit=1, rerank="float")
        assert index.batch_search(rerank_depth=1, **settings)["q"][0].id == "same-sign"
        assert index.batch_search(rerank_depth=2, **settings)["q"][0].id == "closest"
