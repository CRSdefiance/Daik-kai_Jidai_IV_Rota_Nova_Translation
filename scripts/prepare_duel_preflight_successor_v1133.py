"""Reject overlong paragraphs before writing the owned scratch area."""
from pathlib import Path


def main():
    old = Path('scripts/duel_layout_native_v1131.c')
    target = Path('scripts/duel_layout_native_v1133.c')
    assert not target.exists()
    source = old.read_text(encoding='utf-8')
    before = "    if (!text[0] || text[0] == ' ') return 0;\n"
    assert source.count(before) == 1
    source = source.replace(before, before +
        '    while (text[pos]) { if (pos == 127) return 0; ++pos; }\n    pos = 0;\n')
    target.write_text(source, encoding='utf-8')
    source = Path('scripts/compile_duel_layout_v1131.py').read_text(encoding='utf-8')
    target = Path('scripts/compile_duel_layout_v1133.py')
    assert not target.exists()
    source = source.replace("duel_layout_native_v1131')", "duel_layout_native_v1133')")
    source = source.replace("duel_layout_native_v1131.c')", "duel_layout_native_v1133.c')")
    target.write_text(source, encoding='utf-8')
    print('Created preflight-bounded native successor;original failed workspace case preserved.')


if __name__ == '__main__':
    main()
