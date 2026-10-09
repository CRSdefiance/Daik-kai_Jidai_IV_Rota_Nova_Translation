# Ceuta and all-route system notice repair: V153

Update, 2026-10-02: the user confirms the reported issue fixed and explicitly
resumes the full translation goal. The pause and pending-Ceuta statements below
describe the original handoff. Preserve V153's repairs in future builds; full
gameplay coverage and canonical promotion are not inferred from one issue's fix.

Broader translation work remains paused. After the V152 handoff, the user
confirms all six previously reported corruption cases are corrected and
supplies an unreadable Raphael notice after landing at Ceuta. They ask to
find and correct other occurrences. V153 is experimental; no promotion,
commit or push is performed for this repair.

## Cause and scope

The clean Ceuta record, `/data/SC0.DK4` B45 R52, starts with one executable
`FE` byte. An older translated record contains `F8 F2` instead, interpreted
as private-use CP932 text. The percent-safety materializer then copied those
damaged bytes from the translated canonical parent. The initial faulty
authoring transformation has not been reconstructed; a normal CP932 roundtrip
of FE alone preserves FE. The proven fault is the changed command and its
subsequent treatment as ordinary text.
This defect predates the COMMON repacking/copy-alignment regression.

Actual native dispatch at `0202425C` selects framed system-modal consumer
`0205473C` for selector FE. Selector F8 goes to notification consumer
`02053AC4`, consistent with the screenshot's white text on the patterned
background and lost leading characters. The dispatch fixture executes
both branches; UI state preparation and its no-macro text expansion are
explicit contracts. Physical frame composition is not simulated.

An audit of all four routes identifies 13 converted commands, all in
Raphael's opening tutorials:

- B45 R52: Ceuta company market share and trading instruction.
- B46 R51, R54, R58, R62, R65, R68, R72, R76, R80, R83, R87, R91:
  inspecting cities/fleets, battle, searching, icons and mode cycling.

All 13 restore the clean FE selector. The tutorial English is reviewed
against the clean Japanese, with button functions and mode order retained.
Ordinary paragraphs are wrapped by the modal formatter. Ceuta retains its
four semantic fields: city, company, share, instruction. FO remains the
runtime company macro; percent is spelled out to avoid a printf token.
Every record retains its original byte allocation, block size, neighboring
commands and offsets. No other record changes from V152.

The integrated builder now rejects F8 F2 record prefixes in all four
routes. The old materializer refuses the Ceuta progressive-dialogue path.
The source-locked terminal repair requires its native proofs before build.
Future candidate handoffs must verify that saved files match the audit.

## Coverage and limits

- All **1,061 readable FE notices** in the repaired four-route files pass
  actual native modal glyph order, leading/final characters, panel bounds
  and independently decoded full font pixels. Both ASCII and retained
  CP932 punctuation execute. Default name/company expansion is a contract.
- **Eight original empty/nontext states** are preserved: seven FE-only
  records and one exact `FE 0F B1` event payload. They contain no lost prose.
- The original prefix audit's one relocated block exception is checked
  separately: SC0 B44 R264 retains FE and “Received 30,000 gold!”
- The 13 repairs also pass **26 modal render cases**, in both native pixel
  formats. All 13 diagnostic ink previews were visually reviewed.
- Existing one-space modal continuations pass the broader native audit.
  The earlier hypothesis that their guard count necessarily drops a glyph
  is disproven. V153 uses a verified two-space format for the repaired
  notices; healthy notices retain their bytes.
- The V152 shared-copy repair protects **every caller of 020CEC74** by
  dispatching misaligned pointers/counts through the byte loop. Its 3,668
  COMMON selections, 7,336 warm/cold copies and 704 alignment cases remain
  applicable: V153's ARM9 and COMMON are byte-identical to V152. The user
  confirms the original six screenshot cases corrected.

These results establish coverage for the identified command and copy faults.
They do not guarantee every game's screen or customized-name layout. The
modal fixture initializes a native bitmap, executes glyph painting and checks
pixels; emulator frame composition, input dismissal and full gameplay remain
runtime checks. Older record-based evidence must still be revisited with
correct hardware alignment and the actual consumer.

## Experimental handoff

| Item | Exact value |
| --- | --- |
| ROM | `out/all_routes_combined_v153_candidate.nds` |
| ROM SHA-256 | `f9cf6468637e0b578088e4b844fea431806de6827add2388b8cae2e214fb4178` |
| Patch | `out/all_routes_combined_v153_candidate.xdelta` (744,137 bytes) |
| Patch SHA-256 | `5f8e26787fd01475f71ab470df2b7bc9fe5a232c45a33ffcc60c4bd20c351764` |
| Canonical builder base | `out/raphael_natural_v2_accepted_base.nds` |
| Canonical base SHA-256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |
| Clean patch source | `work/clean.nds` |
| Clean source SHA-256 | `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d` |
| Profile | `all-routes-unified-v153`, experimental |
| ARM9 SHA-256 | `21e2be34e965fd17fc56dd18e919e411b7da87a3c8f56f9e7e6fd8c39100940b` |

The build uses the immutable accepted baseline with every accepted layer
automatically included, the complete inherited **435 experimental batches**
and all registered postprocessing stages, followed by the terminal tutorial
repair. It does not use V152 as a binary build parent. V152 is now revoked as
a playable candidate because of the Ceuta defect and retained for diagnostics.

Changed canonical paths are `/COMMON/HELP.DK4`, `/COMMON/MESFILE.DK4`,
`/__arm9__.bin`, `/_pxl/dividecrewinfo.pxl`, `/_pxl/personinfo.pxl`, and
`/data/SC0.DK4` through `/data/SC3.DK4`. **Compared with V152, only the 13
SC0 tutorial records change.** All other components, including graphics,
names, shared-copy repair and the staged ARM7 boot repair, are byte-identical.
The neighboring manifest records the complete lineage and changed records.

Verification passes:

- `probe_raphael_system_panels.py`: 26 glyph/pixel cases and FE/F8 dispatch.
- `audit_all_route_system_panels.py`: 1,061 readable notices; eight
  source-verified exclusions; zero converted commands after repair.
- `verify_raphael_system_panels_v153.py`: exact saved component/record
  preservation, complete manifest lineage, proof/file matches, rejection of
  broken V152 selectors and byte-exact clean-ROM patch reconstruction.
- `verify_release_baseline.py`: expected nine paths, menus and untouched assets.
- Existing native raster regression tests and Ruff pass.

Evidence is in `work/analysis/system_panel_v153_saved_proof.json`,
`work/analysis/all_route_system_panel_native_audit.json` and
`work/analysis/raphael_system_panel_native_proof.json`.
Diagnostic previews are in `work/qa/raphael_system_panels/`.
The user's exact screenshot is preserved in `work/qa/user_ceuta_regression/`;
its candidate/version and savestate use were not explicitly restated.

Cold-boot V153 without a savestate. Check title/New Game, Raphael's Ceuta
notice, all following sailing tutorial notices, and inherited recruitment,
Trader/Barkeep dialogue and Lil's opening. Confirm the frame is readable,
every line starts correctly, the final instruction appears and dismissal
works. Keep this candidate experimental until explicit user acceptance.
