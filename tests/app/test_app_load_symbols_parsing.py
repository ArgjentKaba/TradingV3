import app


def test_load_symbols_parsing_ignores_comments_and_blanks(tmp_path):
    symfile = tmp_path / "symbols.txt"
    symfile.write_text(
        "# comment line\n"
        "\n"
        "  BTCUSDT   \n"  # mit Whitespace
        "ETHUSDT\n"
        "   \n"
        "# another comment\n",
        encoding="utf-8",
    )

    symbols = app.load_symbols(str(symfile))

    # Erwartungen: Kommentare/Leerzeilen weg, Whitespace getrimmt
    assert "BTCUSDT" in symbols
    assert "ETHUSDT" in symbols
    assert all(s and not s.startswith("#") for s in symbols)
