"""Keep a complete five-letter identity for the let's phrase exception."""
from pathlib import Path


def main():
    source = Path('scripts/duel_layout_native_v1128.c').read_text(encoding='utf-8')
    target = Path('scripts/duel_layout_native_v1131.c')
    assert not target.exists()
    before = '    if (length > 5) return 0;'
    assert source.count(before) == 1
    source = source.replace(before, "    if (length > 5 || (length == 5 && lower(text[a]) != 'l')) return 0;")
    target.write_text(source, encoding='utf-8')
    print('Created full-word-identity successor;original compiled source preserved.')


if __name__ == '__main__':
    main()
