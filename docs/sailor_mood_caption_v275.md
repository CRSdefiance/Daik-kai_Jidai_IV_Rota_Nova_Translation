# Natural English Mood caption: combined V275

## Source context and change

The original Sailor Info Mood0 label is **ハイ**. The inherited English label
**High** is ambiguous as an emotional description. The original native effect
routine `02065968` writes Mood0 and then selects positive battle messages
2147–2154, including 「戦闘ですね！」 and 「戦闘なら私の出番ね！」.
Its distinct Mood1 branch selects confidence messages 2155–2162.
The emotional context supports **Excited**, which is natural English and retains
the source enthusiasm. The interpretation comes from the source state/effect
and message pairing; the actual battle event has not been traversed in this audit.

V275 replaces `High` with `Excited` in the **same eight-byte slot** at ARM9
offset `001482F4`. Seven data bytes differ; the final NUL remains in place.
The table pointer, native code, record sizes, every other string, font and
palette are unchanged. No allocation growth or new runtime helper is needed.

## Verification

- The complete preceding V272 profile reproduces byte-for-byte through the
  updated shared builder.
- Every original/current selector value and fallback remains exact. All 13
  status labels execute Sailor Info's actual text routine `020D5404` with
  controlled native bitmap/context inputs. All seven Excited cells and all
  **89 independent font ink pixels** survive within a 48×16 region.
- Odd-length text emits a final blank cell; its ink is empty, and the input,
  header, pixel bounds, registers and stack remain intact. The blank does not
  overwrite the leading or final visible letter.
- The other 12 status rasters, positions and return values are exact to V272.
- A fresh **32,200-frame cold boot** replays the exact controller/stylus town,
  Tavern and five Sailor Info paths. All **97 comparable whole screenshots**
  are unchanged, including title/selection/story/town and the observed plaques.
- All **467** inherited batches, required stages and prior changed records
  remain in the manifest. Every ROM file, artwork, route, ARM7 and overlay is
  exact to V272; only the eight-byte ARM9 label slot differs.
- The clean-ROM xdelta reconstruction is byte-for-byte equal to the candidate.
  Targeted Python files pass Ruff.

The replayed officers remain Healthy/Normal. These captures prove regression
preservation, **not** an actual gameplay display of Excited. That display remains
pending; the native glyph result is explicitly a controlled-input test.

## Registered experimental candidate

| Item | Identity |
|---|---|
| Profile | `all-routes-unified-v275` |
| Candidate | `out/all_routes_combined_v275_candidate.nds` |
| ROM SHA256 | `94fa82c8edd99de4f21829bc94b1b98013929f98cc1378c73fe0768e1d1caddf` |
| Patch | `out/all_routes_combined_v275_candidate.xdelta` |
| Patch SHA256 | `525ed6f36b125362ef0b6f208b8fd5b3853a3349426a1b368036551bc06b00d0` |
| Canonical base | `out/raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch input | `work/clean.nds` |
| Clean SHA256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Changed internal component versus V272 | ARM9 label data only |

The candidate is experimental. Actual Excited gameplay display and user cold-boot
acceptance remain pending; the canonical baseline is unchanged. For later
acceptance, check title/New Game, established story/town, Sailor Info, an officer
whose Mood is Excited, and the earlier tooltip/system-notice repairs.

All **18 plaque/hint entries and Armor/Weapon variants remain incomplete**.
Other alternate status contexts, the confusion/injury-severity wording review,
occupied weapon/armor displays, naming consistency, native/art consumers and
final whole-goal verification remain open. The user's low-resolution Online
image translation exclusion remains in force. Revisit older record-based checks
at actual goal completion. The goal is active and incomplete.

## Evidence

- `translations/sailor_mood_caption_release_v1.json`
- `work/analysis/sailor_mood_v275/native_proof.json`
- `work/analysis/sailor_mood_v275/saved_release_proof.json`
- `work/emulation_v193/sailor_mood_v275/capture_report.json`
- `scripts/verify_sailor_mood_native_v275.py`
- `scripts/verify_sailor_mood_release_v275.py`

This is targeted emulator verification, not a full route or physical-device test.
