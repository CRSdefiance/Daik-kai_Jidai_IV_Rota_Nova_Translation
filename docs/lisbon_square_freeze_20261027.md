# Lisbon Square freeze: font scratch-buffer collision

The user's `font_v2_all_punctuation_one_pixel_20261027_test.nds` freezes while entering Lisbon's Square after Rafael's tutorial. The crowd alert is a normal shared town message. The failure is in Square label drawing, not a diagnosed change to that event's script.

## Confirmed cause

The inherited Square caption painter at `01FFC388..01FFC504` uses a 448-byte temporary bitmap at `01FFC1A0..01FFC360`. The experimental font drawing/footer helper occupies `01FFC200..01FFC300`, inside that bitmap. Static zero bytes in the Square buffer were incorrectly treated as unowned helper storage.

The supplied `desmume-0.9.13-win64/States/LisbonFreeze.dst`, SHA-256 `400297967dd5ad863ae86d07795158a6a30b95d24a863615445d404d54340d7f`, was parsed read-only. Its temporary bitmap header is `[4,17,12,1218688,20]`; the 256-byte font helper span is entirely zero, differing in 138 bytes from the ROM. The saved ARM9 instruction address is `02192D50`.

A separate fresh boot of the reported ROM, with ordinary Rafael opening and town inputs and no savestate or gameplay fixture, independently reaches a blank Square at frame29600 and reports `Undefined instruction: 0x73000000 PC=0x02192D4C`. This ordinary Square visit has50-percent rival influence and no claim to reproduce the user's exact60-percent tutorial/event state. It reproduces the same drawing collision and fault address region.

## Repair candidate

- ROM: `out/font_v2_square_scratch_fix_20261027_test.nds`
- SHA-256: `89860905d61e348ae053d40836159bc86bff5d85d3206ce3a0961a6d60142077`
- Manifest: neighboring `.manifest.json`
- Profile: `font-v2-square-scratch-fix-20261027`, experimental
- Immutable construction base: `out/raphael_natural_v2_accepted_base.nds`, SHA-256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`
- Complete predecessor: the reported all-punctuation test, SHA-256 `fbbd68ee7d1af28ec4656262e53836c52b502c3c2cd0a3dbeddd2646e98342fe`

The integrated builder retains560 manuscript/config entries and114 accepted layers baked into the canonical base. Only `/__arm9__.bin` differs from the reported test ROM, solely within the existing380-byte Square painter. All font glyphs, drawing/footer helpers, spacing, translated text, other executable instructions, graphics, other files/components, section extents and staged payload remain exact.

The painter now uses a448-byte local stack buffer after its unchanged contract guards. It initializes the complete428-byte header/pixel area, passes that temporary view synchronously to the native painter, copies the resulting64x12 caption back, restores the original view and stack, and returns. Eight saved registers plus448 bytes retain eight-byte stack alignment. Original fallback branches run before allocation. Native high-water usage including nested painters is752 bytes.

The three earlier one-pixel font profiles are marked revoked for the demonstrated overlap; their ROMs and producers remain preserved. The canonical baseline, accepted layers and promoted V4701 pointer are unchanged.

## Verification

All18 full native caption planes match independent font masks with the retainedY+1 origin, complete first/final glyphs, original context/header restoration, memory guards and saved-register/stack ABI. The complete4096-byte helper section remains unchanged and there are no writes into the former static scratch span. Four nonmatching width/origin cases retain exact predecessor fallback output/context. The exact predecessor fails the native regression. No font/glyph implementation is stubbed.

The existing integrated-release/font test suite passes29 tests. The baseline verifier, complete predecessor internal-file comparison,560-entry manifest,114 baked-layer registry, canonical hash, release checks and exact proposed ARM9 comparison pass. A first build completed ROM/manifest verification but its console JSON print hit Windows' default encoding; repeating with `PYTHONUTF8=1` exits successfully and produces the same ROM hash.

The repaired candidate completes33100 fresh-boot frames using the same141 ordinary inputs through the failing Square visit, followed by normal menu/return/reentry inputs. Six complete pre-Square frames match the failed ROM exactly: captain selection2600, opening15000/19600, Port27600, town28800 and Square selection29200. Shop labels, the complete initial dialogue, the Trends menu and both returns to town were viewed. Read-only native snapshots before/after Square and after both returns preserve every font and Square instruction. The sole mutable word inside the font helper is its intended footer heap cache at01FFC2D8, which retains the same valid allocation throughout. There is no battery preload, loaded savestate, gameplay fixture or callback error. This verifies ordinary Square entry/return; the user's exact60-percent tutorial/crowd eligibility state was not replayed.

The stable runtime copy is byte exact to the candidate; it was used because the UTF-8 build retry was still running when the replay began. `actual_runtime_proof.json` binds that copy to the final candidate hash. Evidence and exact ordinary input schedules are under `work/lisbon_square_freeze_20261027/`. No full route or hardware verification is claimed.

The final builder also rejects the original collision in any newly derived profile that retains the overlapping font hook without the exact per-call Square painter. Both the broken-ROM negative and repaired-ROM positive pass. Registry serialization preserves the original CRLF convention. The final manifest is regenerated after adding this release gate; the tested ROM bytes remain identical.

Final build exits0 and its manifest/source locks match the tested candidate. The repair is pinned by its physicalE-drive path. The required retention preview was inspected to verify that deletion is possible only with an explicit `ApplyPlan`; the preview then stopped safely on the pre-existing C-junction-path pin for `lil_opening_release_v1710/patch_reconstruction_RESEARCH_ONLY.nds`. That pin is unchanged and no ROMs were deleted.

## Playing the repair

Cold-boot the repaired ROM. A frozen savestate restores the overwritten instructions and invalid CPU state, so loading `LisbonFreeze.dst` cannot apply this repair. A normal in-game save from before the failure can be used. Keep the supplied frozen state as diagnostic evidence.

Build reproduction, from the repository root with its existing dependencies and UTF-8 enabled:

```powershell
$env:PYTHONPATH='.;.runtime_deps;.deps'
$env:PYTHONUTF8='1'
& C:\Python314\python.exe -m scripts.build_integrated_release --profile font-v2-square-scratch-fix-20261027 --out out/font_v2_square_scratch_fix_20261027_test.nds
& C:\Python314\python.exe -m scripts.verify_square_font_scratch_20261027
```
