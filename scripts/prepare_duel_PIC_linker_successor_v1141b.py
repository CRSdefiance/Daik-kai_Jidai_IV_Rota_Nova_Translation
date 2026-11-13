"""Use the pinned driver's supported static PIC linking arguments."""
from pathlib import Path


def main():
    source = Path('scripts/compile_duel_layout_v1141.py').read_text(encoding='utf-8')
    target = Path('scripts/compile_duel_layout_v1141b.py')
    assert not target.exists()
    source = source.replace("duel_layout_native_v1141')", "duel_layout_native_v1141b')")
    before = "'-Wl,--entry=duel_draw', '-Wl,--emit-relocs', '-Wl,-Bsymbolic'"
    assert source.count(before) == 1
    source = source.replace(before, "'-Wl,--entry=duel_draw'")
    target.write_text(source, encoding='utf-8')
    print('Created supported static-PIC linker successor;unsupported driver arguments retained in failed predecessor.')


if __name__ == '__main__':
    main()
