from scrydb import Index


def test_default_highlight_returns_marked_document_text():
    with Index.open(":memory:", vec_ext_path=None) as index:
        index.index_documents([{"id": "d1", "text": "green leaves"}])
        assert index.highlight("green")[0].highlight == "<b>green</b> leaves"
        assert index.highlight("green", column=0)[0].highlight == "d1"
