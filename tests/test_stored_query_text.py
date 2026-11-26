from scrydb import Index


def test_each_stored_query_remembers_its_text_field_across_reopen(tmp_path):
    path = tmp_path / "index.db"
    with Index.open(path, vec_ext_path=None) as index:
        index.index_documents([{"id": "a", "text": "cats"}, {"id": "b", "text": "dogs"}])
        index.index_queries([{"id": "q0", "text": "cats"}])
        index.index_queries([{"id": "q1", "question": "dogs", "text": "cats"}], text_field="question")
    with Index.open(path, vec_ext_path=None) as index:
        run = index.batch_search(mode="lexical")
        assert run["q0"][0].id == "a" and run["q1"][0].id == "b"
        assert index.queries["q1"]["text"] == "cats"
        index.index_queries([{"id": "q1", "text": "cats"}])
        assert index.batch_search("q1")["q1"][0].id == "a"
