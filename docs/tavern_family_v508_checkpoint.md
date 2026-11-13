# V508 shared Tavern portrait-dialogue repair

Previous goal turn: progress, normal Athens arrival and exact proof that message
827 dropped the `r` in `our`. V508 repairs the shared formatting policy and
retains the complete V502 integration stack. Status remains **experimental**.

## Repair and natural English

The existing portrait wrapper selected only some Tavern message IDs. Its scope
now covers the complete original 820–873 Tavern family, still restricted to
portrait parent return `02054014`. Original macro expansion runs first.

The common paragraph helper now treats legacy LF/guard whitespace as paragraph
whitespace, then wraps complete words. First rows retain the existing 36-cell
budget. Portrait continuations reserve both guard/pair phases with a 35-cell
content budget. Equipment and other caller budgets remain unchanged. The same
284-byte owned helper, 236-byte output bound, four-row limit, stack buffer,
autoload extent, pool size, fonts and cache layout are retained. No allocation
or new code-bank space is introduced.

Clean827 confirms a pondering reaction, the patron's name, and a friendly toast
to their new acquaintance. Its reviewed `natural-dialogue-v2` English is:

**“Hmm... %s, right? Here's to our new friendship!”**

The wording restores natural punctuation and voice; it was not shortened to hide
the rendering defect. All other COMMON text, native offsets and copy extents
remain exact. Manuscript: `translations/tavern_toast_manuscript_v1.json`.

## Native and actual-ROM verification

- 7,336 real message/caller dispatch destinations compared. Only the 48 previously
  omitted Tavern IDs gain the existing portrait wrapper; other destinations remain.
- 108 supplied short/long printf, wrap and complete native glyph cases pass for
  all 54 Tavern entries. Every visible character remains in order and every word
  stays on a single row. Source/output guards and saved-register/stack ABI pass.
- The clue843 tests use one item and four separate location/direction fields.
  These are supplied layout contracts, not proof of its original argument provider.
  The earlier untyped stress case supplied five long item names and exceeded the
  four-row contract; its preserved fallback limit is documented separately in
  `oversized_direction_stress.json`. Arbitrary over-capacity strings are not cleared.
- All 20 inherited Guild descriptions and the one-day repair message retain their
  complete native glyph order and whole words. Inherited CP932 full-width Latin
  prefixes are checked as complete glyphs, not mistaken for separate ASCII bytes.
- Ten additional F/I-leading substitution cases retain every glyph, covering the
  historical collision between these ASCII letters and executable macro prefixes.
- An exact normal cold-boot replay from the genuine Istanbul save reaches Athens
  and Myrine's toast. No inventory/state/unlock fixture or savestate. The repaired
  rows contain 515 exact ink pixels, including the complete `our` and final period.
  Both start at x22. Changes from the old screenshot are confined to dialogue text.
- All 56 whole fresh-game title/New Game/story/town/Help captures match V502.
- Changed helper/dispatch/width bytes remain exact in resident ITCM after both runs.
- The registered candidate is byte-identical to the captured research prototype.
  Its exact clean-ROM patch reconstructs the full candidate byte-for-byte.

Verifier: `scripts/verify_tavern_family_release_v508.py`.
Evidence: `work/analysis/tavern_family_v508/release_proof.json` and `native_proof.json`.
The source-preservation proof inherits all 921 witnesses through independently
verified exact PXL/FLS container bytes.

## Release identity

- Candidate: `out/all_routes_combined_v508_candidate.nds`.
- SHA-256: `c7b86f93ad034bf5c19aa82a51cecb4194ace6dcdce23e481e67c24074bbfbcb`.
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile: `all-routes-unified-v508`; all 114 accepted layers and all 470 inherited
  experimental batches/stages retained, plus `tavern_family_wrap_v1`.
- Changed from V502: `/__arm9__.bin` and `/COMMON/MESFILE.DK4` only. All 675 PXL/FLS
  files, every other ROM component and prior graphics remain byte-identical.
- Patch base: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- Patch SHA-256:
  `085ae5cc265338aef592dc501f5a27899bd79d231bbff9fc4a95c2904a6b5c35`.

Human cold-boot acceptance is still required for canonical promotion. The full
graphics goal remains active: unresolved legacy/native comic, environmental,
deeper gameplay and other historical gates remain. All 22 historical requirements
and all 18 incomplete plaque entries remain. Revisit older record-based checks at
actual goal completion; this repair does not claim all other dialogue is audited.
