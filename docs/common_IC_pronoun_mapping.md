# COMMON IC pronoun mapping

Clean ARM9 executable evidence maps `IC` to a first-person pronoun, rather than
a character name. Both Japanese alternatives become **I** in natural English;
`ICたち` and `ICら` become **we/us/our**, according to sentence grammar.
No character gender, rank or identity needs to be invented.

## Exact executable evidence

ARM9 loads at `0x02000000`. The substitution routine begins at `0x02053914`.

- `0x02053934` loads `sb` from the literal at `0x02053AB8`: `0x02143A28`.
  The CP932 NUL-terminated string at file offset `0x143A28` is `僕` (`96 6C`).
- `0x02053938` loads `fp` from `0x02053ABC`: `0x02143A2C`.
  The string at file offset `0x143A2C` is `アタシ` (`83 41 83 5E 83 56`).
- `0x02053A44` tests the input byte for ASCII `I`. It reads the following byte
  at `0x02053A4C`, starts with the `僕` pointer, and tests for ASCII `C`.
- For `C`, it calls `0x0207E9B8` with the current character object. That function
  calls `0x0207EB24` and returns the byte at property offset `0x1A`.
  If the result equals one, `0x02053A68` selects `アタシ` instead.
  The property's broader enum meaning is not asserted here.
- `0x02053A6C–0x02053A88` copies the selected string. `0x02053A8C` advances
  the source pointer by **two bytes**, consuming the complete `IC` token.

Source-locked clean slices:

| ARM9 file range (end exclusive) | SHA-256 |
| --- | --- |
| `0x53914–0x53AC4` | `71f0a5626d1992a8e2a2f0fb5a287bb42d719c0861488c64aec7ea5fe5386d87` |
| `0x7E9B8–0x7E9D0` | `3aa4bb7ba550c0e7daab45dd6d3912ebd38c99facaad78be015a422736ccd76b` |

The two code slices and pronoun literals are byte-identical in the clean ROM and
combined V114. Disassembly evidence is retained in
`work/analysis/common_IC_53914.txt`, `common_IC_7e9b8.txt` and
`common_IC_cmp49_windows.txt`.

## Native occurrence inventory

The clean mapped COMMON table has 21 occurrences: messages 527, 566, 792, 1118,
1140, 1257, 1477, 1561, 1610, 1747, 1783, 2132, 2181, 2296, 2501, 2543, 2554,
2560, 2640, 2646 and 2652. Their native boundaries come from the verified ARM9
directory and offset table, not a search-derived insertion range.

For English prose, use the existing full-width narrow `Ｉ` glyph for a literal
capital I so it is not interpreted as an executable macro. There is no need to
retain a Japanese pronoun macro whose alternatives have the same English form.
Single-paragraph English still requires exact-font preview, allocation and saved
native-selection checks. Live selection, wrapping and transitions remain separate
runtime gates; this mapping alone does not prove them.

## Saved V115 repair checkpoint

V115 replaces all 21 occurrences and their eight native neighbors with fresh
clean-source English. All 29 previews are reviewed and all 3,668 saved native
selections compared. `work/analysis/common_IC_v115_exact.json` additionally
checks each IC occurrence and confirms the parser and pronoun literals remain
unchanged. Older mismatched English in 527, 1118, 1140, 1561 and 1610 is repaired.
Runtime review of paired fleet labels in 2543/2554/2560 remains pending.
