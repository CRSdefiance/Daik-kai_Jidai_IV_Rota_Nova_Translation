# Maria portrait, name widgets and runtime calibration

2026-10-07. The previous turn proved four portrait owners and three complete live
crops. V203 supplies the fourth portrait and Maria name-field evidence through an
explicit native selection fixture. **V190 remains the registered candidate; the
full graphics goal remains active and incomplete.**

## Why the original fresh-game test skipped Maria

The unchanged predicate at `02046DFC` reads a stored halfword at offset `0x38` and
returns whether any of its four low bits is set. The captain constructor calls
that predicate, then at `0209F068` executes `MOVEQ r0,#3` and writes the resulting
selection limit to its object. When the predicate returns zero, the fresh list
therefore contains three captains, explaining the earlier third-RIGHT return to
Rafael. This establishes the selection condition; it does not identify every
writer of those flags or prove a legitimate route-completion unlock.

The research fixture changes only that instruction's immediate value to four:
`03A00003` → `03A00004`. This is **one ARM9 instruction byte** after the separately
guarded five-field name transform. The predicate, save data and all other code
remain unchanged. All scripts, graphics and ARM7 are exact to V190. Native checks
cover 128 combinations of original/fixture code, 16 low-flag states and four
supplied preceding count values. Save flags, stack and unowned object bytes remain
intact; only the intended zero-predicate count differs.

This is a test-only exposure of the fourth captain, not an ordinary gameplay ROM
or a legitimate unlock. Do not register, distribute or use it as a release parent.
The fixture manifest records the exact source, name edits, opcode, native tests
and purpose. No emulator memory injection or savestate is used.

## Complete native display

Ordinary START/A/RIGHT inputs select Maria and show her confirmation screen after
a real cold boot of the fixture. All **14,144 portrait pixels**, including every
edge/background pixel, match the unchanged `/_pxl/personbustup03.pxl` resource at
native bounds **[76, 28, 180, 164]**. Combined with V202, all four captain portraits
now have complete static native pixel evidence: **56,576 pixels**, with the fourth
explicitly obtained through this test-only selection limit.

| Native field | Observed text | Bounds | Exact font ink pixels |
|---|---|---|---:|
| Given name | Maria | [89, 220, 119, 231] | 71 |
| Middle name | Huamei | [89, 242, 125, 253] | 85 |
| Surname | Li | [89, 264, 101, 275] | 20 |
| Company | Li Clan | [89, 286, 131, 297] | 70 |

All **246 ink pixels**, complete first/last letters and blank cells match the
original native font exactly. The company field already supplies Li Clan; it
requires no extra edit in this fixture. The saved confirmation screen and a later
original opening-story capture were visually reviewed. Both emulator runs report
no callback errors. These results, together with V198, cover the complete display
of all five changed static name fields; Camille's given name was tested within his
full opening nameplate. They do not approve all downstream dialogue or captions.

## Real player-object macro expansion

A second fresh fixture run confirms New Game and lets the original game initialize
Maria's player object. The read-only exported RAM snapshot is pinned by hash.
The original native expander/getters then execute in that state, without replacing
a getter, supplying fake names or bridging the macro function.

| Macro | Actual default output | ASCII bytes | Native font width |
|---|---|---:|---:|
| FI | Maria | 5 | 30 px |
| FA | Li | 2 | 12 px |
| FO | Li Clan | 7 | 42 px |
| FU | Maria Huamei Li | 15 | 90 px |

All 16 cases (four macros × four source alignments) return the complete expected
bytes/NUL with source/output guards and stack preserved. The prepared Maria
profiles' FI/FA/FO lengths and widths agree with these actual defaults. No prepared
Maria record currently uses FU; this measurement is evidence for a future explicit
calibration, not a silently activated formatter rule. Arbitrary customized names
and every macro consumer's layout remain outside this default-name test.

## Reproducible artifacts and remaining work

- `scripts/prepare_maria_widget_fixture_v203.py`
- `scripts/verify_maria_widgets_v203.py`
- `scripts/verify_maria_runtime_names_v203.py`
- `work/analysis/maria_widgets_v203/fixture_manifest.json`
- `work/analysis/maria_widgets_v203/native_widget_pixels.json`
- `work/analysis/maria_widgets_v203/native_default_macro_proof.json`
- Cold-boot frames/reports/RAM under `work/emulation_v193/maria_widgets_v203/`.

All three scripts pass focused Ruff. The full names/text/artwork migration remains
unregistered. Continue complete editorial/preview and COMMON/help consumer work,
the movie's Hoodlum-to-Hodram replacement, Gallery/biography consistency, four
unfinished Online bodies, legacy/archive/contextual and broader native/gameplay
gates, then one registered combined ROM and exact reconstructable patch. At goal
completion, revisit the older record-based checks as requested.
