# Condition-label clarity V388

Experimental combined candidate. The full graphics goal remains active. All 22
historical requirements and all 18 incomplete plaque/hint entries remain in the audit.

## Source review

| Field/state | Japanese | Previous English | Reviewed English |
| --- | --- | --- | --- |
| Mood 5 | 混乱 | Dazed | Confused |
| Health 2 | 軽傷 | Wounded | Hurt |
| Health 3 | 重傷 | Injured | Wounded |

Confused preserves the mental condition without suggesting a physical daze.
Hurt and Wounded give minor and serious injury a clearer natural-English sequence.
Original actor-state values and effect routines are unchanged. The other ten labels,
including Excited, Normal and Upset, remain unchanged. Source review and rationale
are in `translations/condition_labels_review_v1.json`.

## Storage and native rendering

The old Dazed slot is eight bytes, immediately followed by Spirit. Confused needs
nine bytes including its NUL, so it is not written over that neighbor. Twenty bytes
of aligned data are appended inside the existing reserved4096-byte SDK autoload
area. Its extent increases from3880 to3900, leaving196 bytes. No new executable
code, arena adjustment, font, palette, viewport or sprite change is introduced.

Only three lookup-table pointers change. Confused and Hurt point to the new reserved
strings; serious injury reuses the original terminated Wounded string. Every old
string byte, including Dazed, Injured, Spirit and Luck, remains exact. Earlier SDK
sections and every preceding reserved-area byte remain exact. Only the SDK's normal
autoload metadata changes alongside those three pointers and new data.

All512 native selector cases preserve actor inputs, stack, saved registers and
fallbacks; only the three intended valid-state results differ. All13 labels render
through original D5404 directly from their actual original or reserved-area string
addresses. Complete48x16 masks, first/final letters, source and bitmap guards pass.
Confused's eighth character is complete at the native width boundary. The other ten
rasters are exact to V383. The preview sheet is an isolated native render, not a
gameplay screenshot, and is excluded from the guide archive.

## Final candidate evidence

- Registered builder retains every470 V383 batch and every earlier native stage.
- Only ARM9 differs from V383. All graphics, COMMON/HELP/routes, ARM7, overlays and
  other components remain byte-exact.
- Final ROM matches the prepared research ROM exactly; clean-input patch reconstructs
  it exactly.
- Twenty-three ordinary New Game frames and42 saved-game officer frames are unchanged
  from their verified controls. The four officer views still show their genuine
  Healthy/Normal/Upset states. New alternate states are not forced into gameplay.
- Actual cold-boot RAM and read-only ITCM exports contain the exact three new lookup
  pointers and complete Confused/Hurt/Wounded strings. This separately proves that
  the real SDK loader delivered the reserved-area data.
- Targeted Ruff, builder syntax and native/full-release verifiers pass.

The release verifier initially had a copied baseline-hash typo; correcting that
constant restored comparison to the independently verified canonical hash. No ROM
change was required for that verifier correction. C-drive disk pressure was handled
with lossless NTFS compression of generated ROMs, checking each hash before/after.
The user's subsequent request moves generated ROM packages to E with verified copies
and directory junctions, preserving the existing logical build paths.

Proofs: `work/analysis/condition_labels_v387/native_proof.json`, `plan.json`, and
`work/analysis/condition_release_v388/release_proof.json`.
Scripts: `prepare_condition_labels_v387.py`, `verify_condition_labels_v387.py`,
`verify_condition_release_v388.py`. The raster helper's optional native-pointer mode
leaves its existing default behavior unchanged and checks source bytes without
writing over code/data neighbors.

These are targeted native and cold-boot emulator checks, not full routes or hardware
tests. Actual Confused/Hurt/Wounded gameplay, occupied Weapon/Armor, other contexts,
legacy consumers and deeper Gallery/endings remain open. All 18 plaques/hints remain
incomplete by user instruction. Revisit older record-based checks at full completion.

## Handoff

Candidate: `out/all_routes_combined_v388_candidate.nds`.
SHA-256: `1629f2823aa953507c0ec3029556701509fd28d364824aefb6ce2aa61109abcc`.
Patch: `out/all_routes_combined_v388_candidate.xdelta`.
SHA-256: `d492edf66385741ee3859a213d0a55051692445008849008b164ba7f4ae74e6f`.
Patch input: `work/clean.nds`, SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

Canonical base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
Profile: `all-routes-unified-v388`. Accepted layers remain baked into the base;
all470 inherited experimental batches and V383 stages remain. Added reviewed stage:
`translations/condition_labels_v1.json`. Full identities/internal records are in
the neighboring manifest. No canonical promotion occurred.

User cold-boot checks: title/New Game, established story/town, Sailor Info across
captains and condition states, Assign Sailors and the ongoing equipment variants.
Experimental pending explicit acceptance. Verified release copies go to
`E:\Rota Nova translations`; generated packages retain their structure under
`E:\Rota Nova translations\Generated` after the requested storage migration.
