# Reverse-engineering notes

Record confirmed ROM hashes, candidate internal paths, compression, encoding, pointer-base
hypotheses, font resources, emulator observations, and screenshots here. Do not add extracted
copyrighted bytes.

Pointer-table rewriting is intentionally deferred until a real fixed-length menu replacement
has booted successfully.

## Confirmed findings

- Clean game code: `ADKJ`; title: `DK4 ROTANOVA`.
- Clean-ROM SHA-256:
  `f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
- The title menu, controller prompts, character values, and biographies are CP932 text
  in ARM9.
- Uppercase and lowercase ASCII render correctly in the existing font.
- The standard font path is mapped in the clean ARM9. `ARM9+0xD169C` advances
  single-byte glyphs by 6 pixels; `ARM9+0xD1674` advances Shift-JIS glyphs by 12.
  The embedded ASCII table begins at `ARM9+0x125A60`, covers codes `0x21` through
  `0x7F`, and stores 11 one-byte rows per glyph. The renderer reads six pixels from
  each row. Space is blank but retains the same 6-pixel advance.
- `/GRP/KANJI.FNT` is exactly 73,480 bytes: 3,340 records of 22 bytes. Each record is
  a 16-by-11 one-bit glyph. The sorted 3,340-entry Shift-JIS-to-glyph map begins at
  `ARM9+0x125EC4`. The loader at `ARM9+0xD1A50` reads the complete `0x11F08`-byte file.
- Standard story dialogue uses a 16-pixel line pitch and a cold-boot calibrated
  216-pixel content width: exactly 36 fixed-width ASCII cells. A 38-cell SC0 probe
  wrapped two cells and a 39-cell probe wrapped three. A separate Market Info probe
  established the same 216-pixel/36-cell width for shared messages. The help-window
  bound still requires separate calibration.
- ARM9 fixed-width replacements boot and display in emulator.
- Biography lines use delimiters that should be preserved with exact-width replacements.
- Five character-row labels appear to be graphics rather than live text.
- Main message candidates remain `/COMMON/MESFILE.DK4` and `/data/SC0.DK4` through
  `/data/SC3.DK4`.
- `MESFILE.DK4` is an `ILNK` container with 41 blocks, 42 offsets including an end
  sentinel, and 2,807 Japanese null-delimited records.
- The only control byte observed inside decoded MESFILE records is `0A` (line feed).
- Some records concatenate multiple messages, so block-offset rebuilding alone does not
  yet prove that expansion is safe; exact-length insertion remains the default.
- `SC0.DK4` through `SC3.DK4` are also ILNK containers. Their block counts are 343,
  325, 336, and 303, respectively.
- Strict CP932 extraction currently yields 6,768, 5,166, 6,608, and 5,010 Japanese
  records from SC0 through SC3. Undecodable segments are preserved and reported rather
  than decoded with replacement characters.
- Parse-and-rebuild roundtrips are byte-exact for MESFILE and all four SC containers.
- Emulator testing of the first Raphael scene confirms that story line-feed bytes must
  remain at their original record-relative offsets. Moving a `0A` earlier causes the
  next English character to appear on the preceding line. Translation rows therefore
  use aligned tokens such as `{LB@31}`.
- Runtime placeholders complicate that rule: `FI` occupies two source bytes but expands
  to the protagonist's full given name. Lines containing it require extra visual spacing
  and emulator review. Source `0A` controls should be retained, but a later control may
  be placed after the completed English sentence when copying the Japanese break would
  create an unnecessary extra English line.
- A live Raphael probe confirms `FI` = given name (`Raphael`), `FA` = family name
  (`Castor`), and `FO` = company name (`Castor Co.`). Their widths follow the normal
  per-glyph advances and therefore vary with edited values. Standalone `I` produces a
  full-width Japanese first-person pronoun (`僕` for Raphael), not a literal English I.
- The routine at `0x020D54F4` recognizes `0A`, calls helper `0x020D596C`, and advances
  past the byte at `0x020D550C`, but cold-boot testing proves this is not sufficient to
  model progressive story display timing. Bare `0A` moved the next glyph to the prior
  line in multiple records. Live-safe story encoding therefore remains `0A 20`; the
  following space is sacrificial. Other renderer families retain separate profiles.
- The narrow two-byte draw path around `0x0207CFD0` is also not the active progressive
  story renderer for SC0 block 44. Patching its buffer terminator and source/column
  increments to consume one ASCII byte at a time had no corrective effect in a cold-boot
  test: the first post-LF glyph still appeared before the transition. Treat this address
  range as a false lead for story newline repair. Future work requires a live emulator
  breakpoint or trace that proves the executing call site before another ROM probe.
- Uppercase `F` is the runtime-substitution command prefix, not a safe literal story
  glyph. `FI`, `FA`, and `FO` are intentional substitutions; ordinary English must
  rewrite capitalized words such as “Father,” “Fine,” and “Forget.”
- In the story renderer, uppercase ASCII `I` is interpreted as a Japanese first-person
  macro rather than a literal Latin glyph. Prose must avoid standalone `I` and words
  beginning with uppercase `I` until that command is fully mapped.
- The character-selection field labels and birth-date suffix are ordinary ARM9 text,
  but live in a second table separate from the character records. The complete date
  formatter is `%2d月%2d日　生まれ`; replacing the formatter removes the month/day
  characters without a graphics edit.
- Trading-post category labels are also ordinary ARM9 text. The category and the
  Japanese `%s店` suffix are stored separately, so complete visible phrases do not
  occur in the ROM.
- The visible stone-panel character labels and city-information plaques remain
  Japanese even when both known ARM9 label tables contain English. Several other
  short captions (`シェア`, `特産品`, `売却品`) have no standard-encoded ROM string.
  These elements belong to the graphics/custom-renderer investigation rather than the
  fixed ARM9 text profiles.
- Trading details use the format `%s\n%s%4d％`. As in dialogue windows, the renderer
  consumes the first single-byte glyph after LF. The English profile inserts a layout
  space after LF so `Flavor` begins intact on the second line.
- The Sound Setup BGM selector contains 38 logical titles packed into
  `/COMMON/MESFILE.DK4` block 36 records 46-63. Their 16-bit block-relative
  interior-offset array begins at ARM9 offset `0x143276`; the translated records
  and regenerated offsets are source-locked in `translations/sound_bgm_titles.json`
  and `translations/sound_selector_arm9.json`.
- The Sound Setup SFX selector is a separate ARM9 table beginning at `0x16ED80`.
  It contains 4 four-byte compact labels, 44 eight-byte slots, and 8 twelve-byte
  slots, plus a standalone `ゲームオーバー` caption at `0x16EFB4`, for 57 titles.
  The compact labels are `帆`, `嵐`, `雨`, and `雷`; their
  three-character English forms are required to retain a null terminator.
  `scripts/verify_sound_selector_build.py` independently checks every translated
  slot and all 38 reconstructed BGM slices.
- Every packed BGM pointer must be even. Odd pointers reproduce the observed
  leading/trailing-letter corruption (`rEndin`, `aBeyondHorizo`). Padding after
  the final title is rendered as part of its field and causes left-shifted text,
  so the packer places all spare bytes before the first pointer in each record.
- Even-aligned narrow ASCII is still not sufficient for the BGM panel. A live v2
  test rendered `Naval Battle` as fragmented/reordered glyph tiles because this
  selector uses a double-byte Japanese glyph path. V3 keeps the original pointers
  and exact title cell spans, replacing each Japanese glyph with a centered CP932
  full-width Latin glyph. Complete narrow track names require a later renderer hook.

## Graphics resource findings

- The visible character-selection labels are confirmed in `/_pxl/charselect.pxl`.
  This is an 8-bpp, BGR555-paletted atlas measuring 256 by 314 pixels; the five label
  masks occupy its final 78 rows.
- The city-information plaque captions are confirmed in `/_pxl/towninfo.pxl`, an
  8-bpp, BGR555-paletted 256-by-192 atlas. The graphics can be decoded and repacked
  without changing the resource dimensions or palette table.
- `FLS/M20.fls` through `FLS/M32.fls` use LZ10-compressed palettes and texture images,
  but inspection shows that they contain cutscene/movie art rather than the menu-label
  graphics.
- Cutscene subtitle cards were found as separate 4-bpp textures in `M22.fls` and
  `M24.fls`. The Japanese Rekoeition production card is a separate texture in
  `logo.fls`. These five textures can be recompressed into their existing slots without
  altering any animation records or illustrated frames.
- Additional shared 8-bpp interface atlases with baked captions include
  `chihofleetinfo.pxl`, `dividecrewinfo.pxl`, `fleetinfo.pxl`, `forceinfo.pxl`,
  `goldsearoutediscovery.pxl`, both Golden Route logs, `personinfo.pxl`,
  `saveloadinfo.pxl`, and `shipinfo.pxl`.
- The six Common radial-menu captions are baked white glyphs in
  `/_pxl/__marker.pxl`. They are not the similarly named ARM9 strings. The
  English graphics pass erases only palette index 15 inside the six caption
  boxes, preserving the brown/gold button art beneath them.
- Ship names, classes, and prices use separate live ARM9 formatters. Removing
  the `号` and `級` suffixes and replacing `金貨%10d枚` with `%10d coins`
  fixes all three verified ship-display paths without altering saved names.
- Ship models are not held in one master array. The validated profile currently
  covers 119 duplicate slots spread across event, catalog, shipyard, fleet, and
  scenario pools, with fixed widths of 8, 12, 16, or 20 bytes.
- The packaged-ROM audit confirms that `/_pxl/__marker.pxl` contains the English
  Common captions after every build stage. A Japanese Common wheel from this ROM
  therefore means the emulator retained the old atlas in memory; cold-booting the
  ROM reloads the translated resource.
# DeSmuME live trace fixture

The early-Raphael savestate `dialogue_live_save_v3.dst` is now the canonical
runtime fixture for the standard-dialogue renderer. Offline savestate parsing
locates `Prince Henry and Duke Leon` at ARM9 address `0x0218F362` and
`Behold, the Carteira` at `0x0218F4DF`. Use
`scripts/desmume_dialogue_renderer_trace.lua` and follow
`docs/desmume_runtime_trace.md` before attempting another ARM9 renderer patch.
# Runtime proof: protected newline renderer (2026-08-12)

The DeSmuME trace captured the live early-Raphael standard-dialogue path:

- `0x02029B30` / `0x02029B48` scan the selected record before display.
- `0x02053914` expands/copies the selected string; the ordinary byte-copy loop is
  `0x02053A94` / `0x02053A9C`, called from `0x020242C8`.
- The final standard-dialogue layout routine is the previously identified
  `0x0207CE98` loop. Narrow characters are normally rendered in two-byte pairs.
- Its explicit LF branch is `0x0207CF14` -> `0x0207CFBC`. The original
  instruction at `0x0207CFC4` advances the source by one byte.
- Its width-boundary LF handling is at `0x0207D034`; the original conditional
  instruction at `0x0207D038` also advances by one byte.

The trace directly showed the stored sequence `0A 20` being copied and read as
two distinct bytes. Therefore the visible continuation-line indent is the
literal guard space, not a renderer-supplied left margin. The guard is still
needed in unpatched builds because narrow English text is pair-oriented.

The attempted experiment retained `LF + SPACE` in translation data and routed
the two LF source advances through a guard-aware helper at `0x02172300`.
That builder is now revoked: independent savestate inspection proves the helper
address is live structured data despite being zero-filled in the ROM image.
`scripts/build_protected_newline_renderer_probe.py` now hard-fails.

The first guarded-layout probe eliminated post-LF letter loss but did not remove
the visible continuation indent. Later cold-boot probes froze after New Game.
The cave-safety trace corrected the root-cause analysis: the probes overwrote
runtime-owned structures, rather than proving that advancing `r9` was invalid.

The follow-up resume trace showed that `0x020D5404` does not return at LF. At
`0x020D550C` it advances r9 from the LF byte to the guard space and immediately
continues processing; the guard is drawn as a normal six-pixel ASCII space. It
then advances to the first real continuation glyph without a second invocation.

Do not globally compensate the cursor at `0x020D5504`. A cold-boot cursor probe
that subtracted six pixels there broke the New Game transition while music kept
playing. `0x020D5404` is a shared renderer used by menu/transition text as well as
story dialogue, so even guard-conditional cursor changes at this global site are
unsafe. The failed builder and ROM were removed. Any future renderer hook must
be scoped to the proven standard-dialogue caller (`LR=0x02054928` in the trace),
or the one-cell guard indent must remain as the safe compatibility tradeoff.

The revoked caller-scoped experiment patched call instruction `0x02054924` and
used a private byte to limit cursor compensation to the synchronous story call.
Its base, `dialogue_protected_newline_probe.nds`, is also revoked because its
helper occupied live data at `0x02172300`. Neither experiment may be rebuilt.

Cold-boot testing revoked the first implementation: Options worked, but New Game
froze with the title background still visible. A subsequent read-only comparison
trace on the then-current protected-newline ROM recorded two LF events returning to
`0x020D57E4` and **zero** entries through the story call at `0x02054924`. This
corrects the first diagnosis: New Game does not use the story call site.

Register preservation was not the root cause. The cold-boot trace found the
supposed private flag at `0x021723FC` already contained `E0`, and the entire
`0x021723FC` through `0x02172463` area held live structured data. The old helper
overwrote those structures. Independent inspection of the known-good Raphael
savestate found different structured data at `0x02172300` through
`0x0217231F`, invalidating the earlier guard-helper location too.

Treat the complete ROM-zero tail `0x02171E48` through `0x02172463` as
runtime-owned. Both historical builders now hard-fail. A future stateless hook
at `0x020D550C` must use a separately verified executable location or a
cave-free relocation.

The cave-free follow-up rewrites the existing `0x020D5504` through
`0x020D556B` LF decision block in place. Its four bounds checks are logically
equivalent to the original nested flag construction, and its successful path
leaves `r0`, `r1`, and `r8` equal to one, `r2` holding current Y, and `r3`
holding lower Y, matching the original state before `0x020D57FC`. The rewrite
uses no runtime storage and leaves the forbidden tail untouched. The disposable
candidate was `out/dialogue_guard_skip_inline_probe.nds`.

Cold-boot screenshots rejected the candidate. For each stored protected break,
the first continuation glyph appeared at the end of the preceding line while
the remainder started flush left on line two. An automatic wrap elsewhere was
flush left and intact because it did not use the stored `LF+SPACE` path. The
guard therefore participates in progressive glyph timing; consuming it at
`0x020D5504` is invalid even when pointer and bounds behavior are otherwise
preserved. The candidate and builder are revoked.

The subsequent read-only cursor trace measured four protected breaks. At LF,
the cursor became zero; at the guard-space iteration it remained zero; at the
first real glyph it was exactly six. The next cave-free probe therefore retains
the original LF and space advancement, routes the ordinary loop continuation
through reclaimed instructions inside the LF block, and resets the cursor only
when the preceding bytes are exactly `0A 20` and the cursor is exactly six.
`out/dialogue_guard_cursor_inline_probe.nds` contains that experimental rewrite
and awaits cold-boot testing.

Cold-boot testing rejected both cursor `0` and cursor `1`: the protected
uppercase `J` in `Janus` was absent. A targeted draw trace then proved that the
one-pixel probe submits glyph `0x4A` at `0x020D5774` with cursor `1`, followed by
`a` with cursor `7`. The failure is downstream of source consumption and cursor
compensation, inside the `blx r3` virtual drawing callback or its clipping path.

# SC0 block-44 relocation evidence (2026-08-20)

SC0 block 44 is a `CS 00 01` compiled-script block. Bytes 4-5 are a little-endian
16-bit logical body length, the logical body begins at byte 8, and the remainder is
zero padding to four-byte alignment. In the canonical SC0 file, block 44 starts at
file-relative offset `0x78E0`, is 6504 bytes long, and declares a 6494-byte body.

The canonical block offset occurs once as an aligned ILNK header entry. The only ARM9
byte coincidence is unaligned across instructions and is not a pointer. A known-good
Raphael savestate contains the block at runtime `0x0218F2B0`; aligned WRAM references
point to the loaded body and current records, showing that these are loader-derived
runtime pointers rather than persistent ROM offsets. The reference inventory is stored
in `work/analysis/sc0_b44_relocation_inventory.json`, and the fail-closed machine map
is `translations/sc0_b44_relocation_map.json`.

The proof rebuild changed only five opening-dialogue segments and the CS length field.
It preserved every other NUL-delimited segment, rebuilt outer ILNK offsets mechanically,
and left the protected ARM9 runtime-owned tail untouched. Cold-boot testing still
rendered only the first expanded box, then skipped directly to town. Therefore NUL
segments are not a sufficient control-flow model: block 44 has an unresolved interior
VM continuation or event target tied to the original byte layout. The relocation map
is revoked and marked incomplete until the CS instruction stream and every target are
decoded.

The known-good savestate stores live pointers outside the loaded block to both command
offset `0x84` and dialogue offset `0x8A`. The failed-build trace then corrected the
initial stale-pointer hypothesis: after displaying the expanded first record, the live
VM pointer advanced to its correct new end at offset `0x66`, not the original `0x53`.
It stopped processing the scene from there. The problem therefore lies in how the VM
parses, aligns, or validates the following compiled command layout, rather than a simple
unchanged continuation pointer. The loaded block also has 1760 zero bytes immediately
after its canonical end, far more than the experiment's 68-byte growth, so collision
with the following loaded block is not the leading explanation. A matching baseline
trace is required to compare the successful post-string transition.

The matching baseline trace supplied that comparison. After the original first record,
the VM resumes at offset `0x54`, where the next command is `00 40 FF FF`. The failed
replacement changed record 13 from 37 bytes (odd) to 56 bytes (even); although its end
pointer was correct, the next command prefix moved from the VM's expected byte phase to
offset `0x67`, while execution resumed at `0x66`. CS dialogue is therefore phase-sensitive
at the 16-bit level. The second probe requires every relocated record to preserve its
source byte parity. If natural encoding has opposite parity, the builder appends one
guarded structural trailing space and records that segment in the release manifest.
