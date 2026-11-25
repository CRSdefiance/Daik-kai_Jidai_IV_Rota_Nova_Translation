ENTRY(duel_draw)
SECTIONS {
  . = 0x02470000;
  .text : { KEEP(*(.text.duel_draw)) *(.text*) *(.rodata*) *(.got*) }
  /DISCARD/ : { *(.ARM.exidx*) *(.ARM.extab*) *(.comment*) *(.note*) }
}
