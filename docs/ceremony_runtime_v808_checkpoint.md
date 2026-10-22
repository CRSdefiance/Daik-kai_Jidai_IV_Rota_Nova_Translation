# V808: bounded ceremony runtime verified

The ceremony selectors and modal result notices fit inside existing audited
runtime allocations. No new source-string tail, section, pool, BSS, cache or arena
allocation is used. The 123040-byte staged payload remains exact.

## Packing and preservation

The existing 168-byte private data bank and contiguous 216-byte formatter/status
bank provide 384 bytes. They now contain an 88-byte ARM/Thumb literal formatter,
80-byte unchanged-semantics status helper, a retained 4-byte entry trampoline,
174-byte selector table, 24-byte halfword phrase index and 14-byte modal filter.
The phrase index requires halfword alignment; every original native halfword
load is verified. The existing modal wrapper remains exactly 128 bytes.

The entry at `02147B98` remains callable by all its previous consumers. The
literal formatter retains the original stack size, macro expander, balanced
word wrapper, copy routine and return contract. The status helper moves within
the already owned bank; its source UI names, all twelve complete English status
phrases and current time phrases remain unchanged. Source/reference closure
preserves every external reference. Earlier speculative source-tail leads are
not used; the ship-label tail had interior references and was rejected.

## Native evidence

- 35,704 exact selector/parent/stride/ABI tests cover the seven prior caller
  contracts and the new ordinary, yes/no and protagonist-table memberships.
- 140 whole-8-MiB status contracts preserve all typed field substitutions,
  registers and guards after relocating the status helper.
- 2,326 paired literal formatter cases produce identical complete output to
  V803, including current ASCII paragraphs, every prospective ceremony expansion,
  empty/indent/LF/CP932 controls and synthetic lengths 1 through 240.
- All 3,668 modal IDs are checked. Only 289, 290, 291, 293, 294 and 295 gain
  balanced wrapping. Other 3,662 outputs and 231 wrong-parent/edge controls match.
  Unrelated notice 292 retains its original path.
- 201 exact-parent ceremony formatting cases and all 32 protagonist-table
  selections match the complete font output inspected in V807. No ID348 proxy
  is used for these final consumer checks.

Evidence: `work/analysis/ceremony_runtime_v808/`. The superseded pre-modal research
is preserved in `pre_modal_probe/`. These are native component tests with explicit
I/O/UI boundaries, not actual ceremony gameplay or new completion credit. The
registered integration is documented in the V809 checkpoint.
