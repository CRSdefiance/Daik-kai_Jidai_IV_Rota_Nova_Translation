# V567: original wooden-header consumers under controlled selection

The production candidate remains V566, SHA256
`5203bd6717a5898cfdcdc200748733a5b677568bfb001614da965b99a312afb3`.
Its ROM, patch, registered profile and canonical parent are unchanged.

## Test input and original code path

V566 proved the two repaired images in a substituted Temporary Storage resource.
This follow-up tests their own original resources instead. Four disposable test
ROMs use V564/control or V566/repaired artwork. Exactly one ARM instruction is
changed at mapped address0208529C: the load of the header-choice field becomes
`MOV r0,#2` for Distributed Goods or `MOV r0,#3` for Spoils. The matching raw-file
offset is located using a unique mapped-code pattern, not an assumed ARM9 offset.

The fixture selects the header while leaving the underlying Cargo Setup state
and actions intact. It does not construct a genuine reward or battle event.
All resource constructors, loaders, getters, palettes and crop/drawing code stay
unchanged. No image, resource file or artwork is substituted. Whole-ROM internal
file comparisons prove that only this one word in ARM9 changes from each parent.
These test ROMs are research artifacts, not playable release candidates.

## Actual resource and display checks

Fresh cold boots load isolated copies of the unchanged source battery save.
Initial and selected-cargo frames4300/4600 provide read-only RAM captures.

| Header | Actual original owner | Actual source view | Actual resident file pointer |
| --- | --- | --- | --- |
| Distributed Goods | 023139E8 | 021914B8 | 0236CDB0 |
| Spoils | 02313A4C | 021914B8 | 0236CDB0 |

These addresses are observed in these separate boots, not universal heap-address
contracts. Each owner occurs in exactly one matching 12-word view, with source
[0,0,256,16] and palette parameter0. Executing original getter020D4170 against each
actual capture resolves a resident PXL byte-identical to its named file in that
test ROM. No manually supplied resource binding or filesystem bridge is used.

All eight control/repaired frame cases pass every banner pixel and every screen
pixel against the independent V566 resource-substitution controls: 32,768 banner
pixels and 786,432 complete two-screen pixels. Both complete English masks,
leading/trailing strokes, original palettes and full crop bounds are included.
The source battery save remains unchanged. Ruff passes.

This verifies original resource loading and display under the explicit test
header choice. Ordinary reward/battle-event reachability, earned items, other
event layout/state variants, a full route playthrough and physical hardware are
not verified. The earlier native-loading gap for these two headers is narrowed;
ordinary event coverage remains a separate open item.

## Evidence and remaining scope

- `scripts/verify_header_consumers_v567.py`: exact one-word fixture preparation,
  original owner/resident-file verification and full native comparisons.
- `work/analysis/header_consumers_v567/fixtures.json`: parent/fixture hashes,
  mapped and raw instruction offsets, before/after bytes and explicit test scope.
- `work/analysis/header_consumers_v567/native_consumer_proof.json`.
- Captures on E under
  `Generated/work/emulation_v193/header_consumers_v567_*`.
- Two screenshots with selection-cheat provenance on E under
  `Screenshots/Test fixtures/V567 Original header consumers`.
  They are not guide-publication candidates.

All 18 original plaque/hint entries remain incomplete. All 22 historical
requirements retain their original scope. Other controls, marker families and
the broader graphics audit remain open; the full graphics goal stays active.
