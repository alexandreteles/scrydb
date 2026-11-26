import pytest

from scrydb import Index


def test_dataframe_inputs_preserve_column_names_and_omit_the_dataframe_index():
    pd = pytest.importorskip("pandas")
    rows = pd.DataFrame([{"doc id": "d", "body": "blue sky"}], index=[100])
    queries = pd.DataFrame([{"id": "q", "text": "sky"}])
    with Index.open(":memory:", vec_ext_path=None) as index:
        index.index_documents(rows, id_field="doc id", text_field="body")
        index.index_queries(queries)
        assert index.batch_search("q")["q"][0].document == {"doc id": "d", "body": "blue sky"}


def test_dataframe_with_duplicate_columns_is_ambiguous():
    pd = pytest.importorskip("pandas")
    ambiguous = pd.DataFrame([["d", "first", "second"]], columns=["id", "text", "text"])
    with Index.open(":memory:", vec_ext_path=None) as index:
        with pytest.raises(ValueError, match="unique column names"):
            index.index_documents(ambiguous)
