"""Create a position-independent cache-resident draw component for research."""
from pathlib import Path


def main():
    old = Path('scripts/duel_layout_native_v1133.c')
    target = Path('scripts/duel_layout_native_v1141.c')
    assert not target.exists()
    source = old.read_text(encoding='utf-8')
    source += '''

/* Only the original reviewed font callback is a fixed external address. */
u8 *duel_draw(u32 *context, u8 *text) {
    int rows = duel_layout(text);
    if (rows) context[10] = rows == 1 ? 12 : 0;
    return ((u8 *(*)(u32 *, u8 *))0x020d5404u)(context, text);
}
'''
    target.write_text(source, encoding='utf-8')
    linker = Path('scripts/duel_layout_native_v1141.ld')
    assert not linker.exists()
    linker.write_text('''ENTRY(duel_draw)
SECTIONS {
  . = 0x02470000;
  .text : { KEEP(*(.text.duel_draw)) *(.text*) *(.rodata*) *(.got*) }
  /DISCARD/ : { *(.ARM.exidx*) *(.ARM.extab*) *(.comment*) *(.note*) }
}
''', encoding='utf-8')
    source = Path('scripts/compile_duel_layout_v1135.py').read_text(encoding='utf-8')
    target = Path('scripts/compile_duel_layout_v1141.py')
    assert not target.exists()
    replacements = {
        "ROOT = Path('work/analysis/duel_layout_native_v1135')": "ROOT = Path('work/analysis/duel_layout_native_v1141')",
        "SOURCE = Path('scripts/duel_layout_native_v1133.c')": "SOURCE = Path('scripts/duel_layout_native_v1141.c')",
        "LINKER = Path('scripts/duel_layout_native_v1128.ld')": "LINKER = Path('scripts/duel_layout_native_v1141.ld')",
        "'-Oz', '-g', '-ffreestanding'": "'-Oz', '-g', '-fPIC', '-fvisibility=hidden', '-ffreestanding'",
        "'-Wl,--entry=duel_layout'": "'-Wl,--entry=duel_draw', '-Wl,--emit-relocs', '-Wl,-Bsymbolic'",
    }
    for before, after in replacements.items():
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    target.write_text(source, encoding='utf-8')
    print('Created PIC layout+original-draw component;cache ownership and native relocation still require proof.')


if __name__ == '__main__':
    main()
