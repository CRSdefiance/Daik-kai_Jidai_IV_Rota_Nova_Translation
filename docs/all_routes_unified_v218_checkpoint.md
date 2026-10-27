# Combined graphics checkpoint V218

## Candidate and ancestry

Experimental profile: `all-routes-unified-v218`.

- ROM: `out/all_routes_combined_v218_candidate.nds`.
- SHA-256: `be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.
- Patch: `out/all_routes_combined_v218_candidate.xdelta`.
- Patch SHA-256: `78a21b599468357488ad2f54ba71a9b25a90be6cb1e375f85612b3e0301c1f7e`.
- Canonical parent: `out/raphael_natural_v2_accepted_base.nds`, SHA-256
  `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Clean patch source: `work/clean.nds`, SHA-256
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.

The full V217 ROM reproduces byte for byte after the builder extension. V218
retains all 467 inherited batches, 114 baked accepted layers and terminal stages.
Only ARM9 changes relative to V217. Every existing ROM file, original overlay,
ARM7, font and palette is unchanged. Applying the patch to the clean source
reconstructs V218 exactly. The candidate has not been promoted or human-accepted.

## Completed notice

Japanese: 戦闘を仕掛ける相手がいません.

English: **There are no targets to attack.**

The sentence describes the absence of an eligible on-screen attack target. It does
not imply that the player is globally at peace or that only individual people can
be attacked. Automatic word wrapping gives two natural rows:

```text
There are no
targets to attack.
```

Both source presentations are covered: the ordinary string referenced at
`0207007C` and the packed graphics producer called at `0207B928`. Original
Japanese fields are preserved as source evidence; the callers select the complete
English presentation. No text is shortened to fit the old Japanese allocation.

## Sprite ownership, bounds and preservation

The original Japanese graphic used six 32x16 banks at Main OBJ offset 4000. That
region overlaps the DSOBJR boot upload, which extends from 4000 to 5520. Extending
the old upload in place would overwrite additional original artwork.

The English graphic uses eight banks at **5600..5E00**, after both original uploads
(DSOBJ 0..3E00 and DSOBJR 4000..5520), within the Main OBJ address space. Its native
tile indices start at 688. The original font and palette index 1 are retained.
An eight-bank draw replaces only the six notice-specific submissions; all other
mode logic and drawing paths remain intact. The full 128x32 notice begins at
(80,272); complete English ink stays inside that region and above the footer.

The ordinary bitmap view is widened to 120x24. Its generated continuation uses
two guard spaces: the native two-ASCII renderer overwrites the first continuation
letter with only one guard. Native glyph checks in indexed and direct-color modes
verify every letter and punctuation mark, including the leading `t` in `targets`,
within the 120x24 view. This is formatter-owned syntax, not manuscript padding.

The original constructor executes with a captured live resource binding and
returns the enlarged dimensions. That captured binding is not a CPU paintable
bitmap; independent native font-pixel checks therefore use the established explicit
generic surface contract, with every glyph bounded to the actual notice view.
This fixture is not presented as a physical rendering proof of that alternate
bitmap consumer. The actual visible packed-sprite notice is verified below.

Native startup, complete staged pool copy/cache maintenance, ARM7 preservation
and the expanded main arena pass. Every other arena bound and all inherited
runtime helpers/graphics bytes remain intact. Native sprite submissions and SDK
VRAM/cache transfers are explicit bridges in the machine-code fixture; actual
emulator capture independently verifies their final display.

## Actual cold-boot and pixel verification

An ordinary V218 cold boot reaches the real empty-target Declare War screen at
frame 18400, without savestates or RAM injection.

- All **304 English ink pixels** and **4,096 foreground/blank pixels** in the notice
  region match the complete generated glyphs. Every first/last letter and period
  is present; no old Japanese glyphs remain there.
- The original notice's 554 native Japanese ink pixels establish the unchanged
  foreground palette color: native five-bit RGB `(8,5,0)`.
- All **94,208 pixels outside the notice** are identical to V217 at the same frame.
  This includes clocks, controls, footer, upper instructions and scenery.
- Four inherited Info/Search/Declare War captures still pass complete glyph and
  blank-mask checks, including both Info entry paths: **180,224 pixels**.
- Title menu, New Game, established story and town frames are each entirely
  identical to the previously reviewed V217 frames: 98,304 pixels per frame.

The complete English notice was visually reviewed and is readable, with natural
word boundaries and no footer overlap. These are emulator results, not physical
DS testing or human release acceptance.

## Artifacts

- `translations/sailing_no_attack_target_manuscript_v1.json`: reviewed logical prose.
- `translations/sailing_no_target_release_v1.json`: exact release source/evidence locks.
- `dk4tool/patch/sailing_no_target.py`: source-locked formatter, graphics, consumers
  and staged pool integration.
- `scripts/verify_no_target_v218.py`: native producer, eight sprite requests,
  original upload bounds, ordinary view/font checks, startup/cache/arena checks.
- `scripts/verify_no_target_live_v218.py`: real notice, original palette, whole
  surrounding frame and four inherited panel comparisons.
- `scripts/verify_no_target_release_v218.py`: complete stack and exact patch checks.
- `work/analysis/no_target_v218/native_proof.json`, `live_pixels.json`, `saved_proof.json`.
- `work/emulation_v193/no_target_v218/`: complete capture report and frames.

Focused Ruff checks pass.

## Full goal remains active

The separate no-target notice is now localized. The four unfinished Online
screenshot bodies/chat, confirmed-name consistency, unclassified embedded/raw
consumers, contextual artwork and native display checks, and final whole-scope
gameplay audit remain open. The alternate ordinary bitmap presentation's physical
use is not inferred from the packed sprite capture. No whole-game guarantee or
graphics-goal completion is claimed. Revisit older record-based checks when the
full goal is complete, as requested.
