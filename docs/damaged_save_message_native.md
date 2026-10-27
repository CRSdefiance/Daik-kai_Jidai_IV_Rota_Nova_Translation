# Damaged-save message: native layout reviewed and integrated in V145

The final generated layout is two complete word-boundary rows, with native
two-space continuation protection. Full prose and slot numbering are unchanged.
All 256 preparations now execute the actual modal formatter/macros; all twelve
native pixel cases preserve every glyph and have no split words. Six final panels
are visually reviewed. Formatting is approved for experimental integration.
The suffix uses 52 bytes including NUL, and the largest tested complete message
uses 58 of its 60 destination bytes. Strict review/source gates integrate it
after V144. V145 saved-ROM/canonical preservation and exact patch reconstruction
pass; see `all_routes_unified_v145_checkpoint.md`. Earlier observations below
describe the unwrapped draft. Full physical gameplay remains pending.

The V144 ARM9 inventory reveals the still-Japanese save-error suffix at 12EB4C.
Its exact original allocation is 52 bytes, copied as 26 byte pairs at EE684–EE6B8
into frame+3C. On a checksum mismatch, EE75C–EE780 converts the incoming slot plus
one to full-width digits, copies the number into frame+0 and concatenates the
suffix. The destination occupies 60 bytes before the separately copied suffix.
The actual caller at EE090 reads an unsigned byte; the probe covers all 256
representable inputs without claiming all are valid save-slot selections.

Original: `番のセーブデータは壊れています\n読み込めませんでした`.
Draft suffix: `: This save is corrupted and could not be loaded.`
The native number precedes the colon. The complete corruption/failed-load meaning
is retained in natural English. Source, context, localization and naturalness
reviews are approved; formatting remains false.

All 256 actual native numeric conversion, copy and concatenation cases pass.
Full-width numbers, complete English, NUL, stack state, destination guards and
adjacent suffix are preserved. Complete results require at most 56 of 60 bytes;
the suffix uses 50 of its 52 owned bytes. No executable code changes.

Twelve native modal raster cases for display numbers 1, 9, 10, 99, 100 and 256 in
both pixel formats preserve every glyph and match independent font pixels. The
unchanged V142 raster/ITCM prefix is checked against V144 before execution. All
six native-ink panels have been visually inspected. The renderer splits `be` for
one-digit numbers and `not` for three-digit numbers. Complete prose must receive
word-aware layout before integration; glyph completeness alone is insufficient.

Tools: `scripts/probe_damaged_save_message.py` and
`scripts/probe_damaged_save_pixels.py`. Both pass Ruff. Manuscript:
`translations/damaged_save_message_manuscript_v1.json`. Proof:
`work/analysis/damaged_save_message_proof.json`. Native sheet/report:
`work/qa/damaged_save_native/`. The proposed ARM9 is disposable research only;
V144 and its patch remain unchanged.

Disk reading/checksum validation, full load-error caller and widgets, input
dismissal, physical routing and cold-boot gameplay remain pending. Native
preparation and modal raster execute in separate invocations.
