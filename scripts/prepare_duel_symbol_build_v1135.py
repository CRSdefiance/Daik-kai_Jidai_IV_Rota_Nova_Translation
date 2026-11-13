"""Retain ELF mapping symbols for ISA audit without changing native code."""
from pathlib import Path


def main():
    source = Path('scripts/compile_duel_layout_v1133.py').read_text(encoding='utf-8')
    target = Path('scripts/compile_duel_layout_v1135.py')
    assert not target.exists()
    before = "ROOT = Path('work/analysis/duel_layout_native_v1133')"
    assert source.count(before) == 1
    source = source.replace(before, "ROOT = Path('work/analysis/duel_layout_native_v1135')")
    assert source.count("'-Oz', '-ffreestanding'") == 1
    source = source.replace("'-Oz', '-ffreestanding'", "'-Oz', '-g', '-ffreestanding'")
    target.write_text(source, encoding='utf-8')
    print('Created symbol-bearing compiler successor for code/data ISA classification.')


if __name__ == '__main__':
    main()
