# Footer-wide complete-character repair V318

## Defect and high-level fix

The shared footer renderer measured ASCII as `floor(byte_count/2)*12`.
Seven-character **Sea Map** received36 pixels instead of42, and the following
label overwrote its final p. The five-character **Sails** command also lost its
last cell. This is a renderer measurement defect, separate from translation prose.

Two original instructions now compute byte_count times6. Even byte lengths,
including12-pixel CP932 pairs, retain their original widths. The original
12-row rendering surface is preserved; no text is shortened or padded to hide
the defect. All other code, descriptor pointers, fonts, staged helpers and
arena extents remain unchanged.

The active自動移動停止 caption is translated as **Stop Auto Move** in its
original16-byte slot. Other related Japanese source literals remain intact
because their active owners already point to English text, as documented in V317.

## Verification

- 129 native byte-length cases0–128 verify exact widths and preserved surface height.
- Both sailing footer layouts and all three Golden Route layouts pass complete
  native pixels/placement in4-bit and16-bit formats:10 cases. The Golden Route
  outputs are unchanged; complete sailing words fit without overlapping letters.
- Six conditional item/Gallery configurations pass in both formats:12 additional
  native raster cases.
- The same ordinary32,800-frame cold boot is replayed on V318 and the exact V316
  parent. Title/New Game, Rafael's opening/town/tutorial and sailing are traversed.
- At frames30400/30800, all96 Sea Map ink pixels and every blank cell match the
  native font at(139,370). Both Sails captions also pass complete font masks.
- 76 comparable whole frames are exact. Nine frames change, including footer
  placement and a dialogue-advance indicator. Four Sea View captures also have
  dynamic sea/HUD rendering differences outside the footer; their dates match
  exactly and the paired scenes were visually reviewed. Their other pixels are
  explicitly not claimed identical. No whole-screen footer-only claim is made.

Initial comparisons used an older untranslated reef-warning baseline and an
overly narrow footer bound. Those assumptions were rejected. The final comparison
uses the actual V316 parent and records the nonfooter animation differences.
Neither ROM nor screenshots were changed to satisfy a comparison.

This is targeted automated emulator evidence, not a complete route playthrough
or device test. Stop Auto Move's actual automatic-sailing context remains open:
the ordinary saved crew does not yet meet the Survey120 requirement.

## Registered experimental handoff

| Item | Identity |
|---|---|
| Candidate |`out/all_routes_combined_v318_candidate.nds`|
| ROM SHA256 |`45b549eafee6a9cf3ff2d8a4e637f8722ebd52fb61dfa9b1dc5adab2fe6d1007`|
| Patch |`out/all_routes_combined_v318_candidate.xdelta`|
| Patch SHA256 |`289212a1ab7fe08e79451af22044423c2948e9cc77a41364b28310ccbf03eec8`|
| Canonical base |`out/raphael_natural_v2_accepted_base.nds`|
| Base SHA256 |`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`|
| Profile |`all-routes-unified-v318`|
| Applied stack |All470 inherited batches, accepted canonical layers and inherited native stages|
| New experimental stage |`translations/footer_measurement_release_v1.json`|
| New internal delta versus V316 |`/__arm9__.bin`: two instructions and the16-byte Stop caption|
| Full manifest |`out/all_routes_combined_v318_candidate.manifest.json`|

Every art/data/route/COMMON/HELP file, ARM7, overlay and banner is exact V316.
Against the canonical base, the inherited changed files remain the41 paths
enumerated in the manifest and [V309 documentation](sailing_condition_names_v309.md).
No accepted layer is removed or promoted. Full V316 reproduces byte-for-byte
before and after the optional builder stage. The clean-input patch reconstructs
V318 exactly. Native length/family/raster, release/inheritance/patch, actual
capture/font and Ruff checks pass.

Experimental; user cold-boot acceptance pending and canonical unchanged.
On the user's emulator, check title/New Game, established town/dialogue screens,
and sailing footer labels, especially both final Sails letters and Sea Map's p.
Check Stop Auto Move when automatic sailing becomes available.

## Current scope

Both graphics audits and progress documents record V318. All18 plaque/hint
entries and Armor/Weapon variants remain incomplete. Legacy raw consumers,
actual hidden Gallery/ending contexts, alternate conditions and occupied
weapon/armor checks remain open. Low resolution Online screenshot translation
remains exempt. The full graphics goal stays active; revisit older record-based
checks at actual completion.

Evidence: `work/analysis/footer_measurement_v318/release_proof.json`,
`item_footer_proof.json`, the V316 reproductions and exact reconstructed ROM;
`work/emulation_v193/footer_measurement_v318/capture_report.json` and the exact
parent capture report. V317 retains source owners,129 native measurements and
the10-family native proof.
