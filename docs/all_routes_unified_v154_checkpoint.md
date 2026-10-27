# Combined V154: ordinary name and role fidelity

## Changes

The user confirmed the V153 Ceuta fix and resumed translation on 2026-10-02.
Experimental V154 preserves that fix and all 435 inherited batches. Seventeen
ordinary names/roles are reviewed against clean Japanese and corrected:

| Indices | Source | English |
| --- | --- | --- |
| 10, 25, 64, 65 | シエン / イファ / ユリス / プレット | Xien / Yifa / Yuris / Plett; established route spellings |
| 131 | 総督 | Governor |
| 134, 136, 137 | 高僧 | Senior Monk |
| 164, 165 | カップル男 / カップル女 | Man in a Couple / Woman in a Couple |
| 169 | 妖艶な女 | Alluring Woman |
| 170 | 謎の老人 | Mysterious Old Man |
| 171 | 研究生 | Research Student |
| 172 | 行き倒れ | Collapsed Person |
| 173 | 怪しい人 | Suspicious Person |
| 185, 203 | ダンディー / さくら | Dandy / Sakura |

The six fitting proper names retain their exact static allocations. The other
labels use the existing aligned persistent pool, expanded by 64 bytes to 1,568
bytes. All 239 inherited references are repacked together; complete unrelated
item/entity strings are preserved. Governor's sole reference is relocated.
The staged loader remains outside ARM7's original image. Heap low rises by
64 bytes; the exclusive BSS endpoint, ITCM, DTCM, fonts and text renderers are
preserved. No old shared-copy or FE formatting rule is weakened.

## Verification

- All 207 actual ordinary-name selections return the expected text; the other
  190 names are unchanged. This is not complete semantic approval of those 190.
- Every byte position in ARM9 and decompressed overlays is audited for owner
  and interior references. The BSS endpoint is classified separately from a
  string reference; all revised shared aliases have the same clean meaning.
- Actual ARM9/ARM7 autoloaders preserve the complete ARM7 source and loaded
  sections. The late startup copy preserves SP/r0–r3 and the full expanded pool.
- All 704 ARM946 copy alignment cases pass; 3,668 COMMON selections and the
  repaired copy code are preserved.
- All 34 revised native name rasters match independent pixels. All 17 panels
  were visually inspected: first/final glyphs present, full labels readable.
- Ten additional native rasters verify the five inherited full-width F names
  (Fernando, Fernan, Follower, Francisca, Faticia) using the actual CP932/ITCM
  painter. All five panels were inspected. Their wider F is a preserved macro
  escape; no normalization or dropped initial is introduced.
- 33 focused name/fleet/caption tests and Ruff pass. Saved component comparison,
  registry/manifest lineage, baseline menus/graphics and clean patch roundtrip
  pass. The inherited 1,061-panel proof is preserved through exact route files,
  fonts and consumer code; it is not rerun against a new whole-ARM9 hash.

Actual actor assignment, other displays, customized names and physical scene
composition remain gameplay checks. Cross-CPU scheduling and full cold boot
are not modeled by the harness. These limitations prevent a universal visual
guarantee or full route acceptance.

## Handoff

- Candidate: `out/all_routes_combined_v154_candidate.nds`
- SHA-256: `56f41c924cc9e9e470a8a0f29a1e7e77069c22d4f7395615b2f640ae2945ac51`
- Patch: `out/all_routes_combined_v154_candidate.xdelta`, 744,178 bytes
- Patch SHA-256: `e865bcd771692b0ae827fcd2e2e4fc4a08c4d43ef1bdc9af37628da72ff685cb`
- Canonical base: `out/raphael_natural_v2_accepted_base.nds`
- Base SHA-256: `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Profile: `all-routes-unified-v154`, **experimental**.
- Accepted content remains baked into the canonical base. The profile applies
  all 435 inherited experimental batches and registered terminal stages,
  including staged boot, shared copy, FE panels and the new name correction.
  No accepted layer is omitted or promoted.
- From V153, only `/__arm9__.bin` changes. From the canonical base, nine paths
  change: ARM9, COMMON HELP/MESFILE, dividecrewinfo/personinfo PXL, and SC0–SC3.
- Cold boot without a savestate: title, New Game, established recruitment/story
  scene, town UI, Ceuta and subsequent tutorials; check revised nameplates as
  encountered. User approval of V153's reported issue is recorded separately.

Proofs: `ordinary_name_fidelity_research_proof.json`,
`ordinary_name_fidelity_paired_pixels_proof.json`,
`ordinary_name_inherited_initials_pixels_proof.json`,
`ordinary_name_v154_saved_proof.json`, baseline and harness logs under
`work/analysis/`; the manifest is beside the ROM.

## Remaining goal

245 COMMON selections/133 owners have reviewed drafts but unresolved actual
consumer/layout integration. Graphics need localization/native composition:
26 PXL/FLS assets, three earlier embedded copies, and one newly reviewed
external-palette CMMNIMG atlas. Two MAPPOINT atlases contain decorative East
Asian glyphs with unresolved context; 21 embedded blocks remain unclassified.
Broader ARM9/UI inventory and older-name fidelity remain open. The Han-script
name readings at indices 201/202 require further context; they are preserved.
Retain the requested after-goal revisit of older record-based checks.

The remaining-COMMON research has additionally been rebased on V154 and passes
798 warm/cold authored/neighbor copy cases with explicit ARM946 behavior. All
3,668 selections are compared. Those drafts are not integrated or approved for
display. Separate artifacts have the `remaining_common_v154_` prefix.

`arm9_text_loaded_inventory_v154.json` inventories all four actual SDK sections
and the decompressed overlay at their real runtime addresses. Its 81,315 byte
candidates include binary coincidences; 1,518 have address-word leads. A saved
237-entry code-reference triage queue includes single-character candidates and
unresolved Japanese UI strings. None is treated as displayed or unused without
consumer evidence. The serialized inventory is also retained for file-offset
comparison. Native allocation and graphic assets remain unchanged by research.

## Goal lifecycle

Translation work is authorized to continue. Automatic continuation now reports
the saved goal as `active`, confirmed on 2026-10-02. The previous paused app-state
condition is resolved. The full goal remains incomplete. New village work is
tracked in `village_promised_words_research_checkpoint.md`; V154 remains the
latest combined playable candidate.
