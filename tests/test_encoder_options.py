import sys
from types import SimpleNamespace

import numpy as np

from scrydb import SentenceEmbedding


def test_configures_the_lazy_encoder_and_both_encoding_paths(monkeypatch):
    loaded, encoded = [], []

    class FakeModel:
        def __init__(self, name, **options):
            loaded.append((name, options))

        def encode(self, texts, **options):
            encoded.append((texts, options, self.max_seq_length))
            return np.ones((len(texts), 8))

    monkeypatch.setitem(sys.modules, "sentence_transformers", SimpleNamespace(SentenceTransformer=FakeModel))
    encoder = SentenceEmbedding("example", 8, "Q: {query}", device="cpu", revision="pinned",
                                batch_size=4, max_seq_length=128)
    assert loaded == []
    assert encoder.encode_documents(["doc"]).dtype == np.float32
    encoder.encode_queries(["q"])
    assert loaded == [("example", {"truncate_dim": 8, "device": "cpu", "revision": "pinned"})]
    assert encoded == [(["doc"], {"batch_size": 4}, 128), (["Q: q"], {"batch_size": 4}, 128)]
