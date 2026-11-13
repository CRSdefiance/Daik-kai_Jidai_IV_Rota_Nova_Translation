ENTRY(duel_layout)
SECTIONS {
  . = 0x02470000;
  .text : { KEEP(*(.text.duel_layout)) *(.text*) *(.rodata*) }
  /DISCARD/ : { *(.ARM.exidx*) *(.ARM.extab*) *(.comment*) *(.note*) }
}
