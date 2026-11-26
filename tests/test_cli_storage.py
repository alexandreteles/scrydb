import pytest

from scrydb.cli import build_parser


@pytest.mark.parametrize("command", ["index", "auto"])
def test_cli_can_select_binary_only_storage(monkeypatch, command):
    monkeypatch.delenv("SCRYDB_STORE_FULL", raising=False)
    parser = build_parser()
    assert parser.parse_args([command]).store_full
    args = parser.parse_args([command, "--no-store-full"])
    assert not args.store_full and not args.store_int8
    monkeypatch.setenv("SCRYDB_STORE_FULL", "false")
    assert not build_parser().parse_args([command]).store_full
    assert build_parser().parse_args([command, "--store-full"]).store_full
