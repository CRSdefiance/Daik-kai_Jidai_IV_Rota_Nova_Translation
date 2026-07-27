# Reverse-engineering notes

Record confirmed ROM hashes, candidate internal paths, compression, encoding, pointer-base
hypotheses, font resources, emulator observations, and screenshots here. Do not add extracted
copyrighted bytes.

Pointer-table rewriting is intentionally deferred until a real fixed-length menu replacement
has booted successfully.

## Confirmed findings

- Clean game code: `ADKJ`; title: `DK4 ROTANOVA`.
- Clean-ROM SHA-256:
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- The title menu, controller prompts, character values, and biographies are CP932 text
  in ARM9.
- Uppercase and lowercase ASCII render correctly in the existing font.
- ARM9 fixed-width replacements boot and display in emulator.
- Biography lines use delimiters that should be preserved with exact-width replacements.
- Five character-row labels appear to be graphics rather than live text.
- Main message candidates remain `/COMMON/MESFILE.DK4` and `/data/SC0.DK4` through
  `/data/SC3.DK4`.
