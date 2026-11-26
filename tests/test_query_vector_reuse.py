import numpy as np

from scrydb import Index


class CountingEncoder:
    def __init__(self):
        self.batches = []

    def encode_queries(self, texts):
        self.batches.append(list(texts))
        return np.ones((len(texts), 8), dtype=np.float32)


def test_stored_precision_skips_encoding_and_dense_misses_are_batched():
    with Index.open(":memory:") as index:
        index.index_documents([{"id": "d", "text": "word", "emb": [1] * 8}])
        index.index_queries([
            {"id": "stored", "text": "stored text", "emb": [1] * 8},
            {"id": "one", "text": "first"},
            {"id": "two", "text": "second"},
        ], store_full_embeddings=False)
        encoder = CountingEncoder()
        index.add_model(encoder)
        run = index.batch_search(["one", "stored", "two"], mode="semantic")
        assert list(run) == ["one", "stored", "two"]
        assert encoder.batches == [["first", "second"]]


def test_rerank_can_use_float_fallback_without_a_model():
    with Index.open(":memory:") as index:
        record = {"id": "d", "text": "word", "emb": [1] * 8}
        index.index_documents([record], store_int8_embeddings=True)
        index.index_queries([record])
        assert index.batch_search("d", mode="semantic", rerank="int8")["d"][0].id == "d"
