import pytest

from scrydb.cli import _search_options, build_parser


@pytest.mark.parametrize("argv", [["search", "words"], ["batch-search"], ["auto"]])
def test_all_search_commands_forward_candidate_settings(monkeypatch, argv):
    monkeypatch.setenv("SCRYDB_CANDIDATE_LIMIT", "90")
    args = build_parser().parse_args(argv + ["--rerank-depth", "300", "--rrf-k", "21"])
    options = _search_options(args)
    assert options["rerank_depth"] == 300
    assert options["candidate_limit"] == 90
    assert options["rrf_k"] == 21
