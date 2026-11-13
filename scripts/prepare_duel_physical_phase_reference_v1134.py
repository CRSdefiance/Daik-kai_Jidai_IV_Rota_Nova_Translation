"""Include invisible native pair flushes inside the actual24-cell view."""
from pathlib import Path


def main():
    source = Path('scripts/duel_postmacro_layout_v1119.py').read_text(encoding='utf-8')
    target = Path('scripts/duel_postmacro_layout_v1134.py')
    assert not target.exists()
    before = '            if width>WIDTH:break\n            tail=solve(end,rows-1)'
    assert source.count(before) == 1
    source = source.replace(before, '            if width>WIDTH:break\n'
        '            if width+trailing_ascii_phase(line)>WIDTH:continue\n            tail=solve(end,rows-1)')
    target.write_text(source, encoding='utf-8')
    print('Created physical-pair-phase reference;whole source words and24x3 bounds preserved.')


if __name__ == '__main__':
    main()
