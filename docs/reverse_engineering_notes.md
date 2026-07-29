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
- Broader emulator testing shows that `0A` is applied after the next single-byte glyph.
  Aligned English breaks therefore encode `0A 20`: the following space is consumed on
  the preceding line and the intended first letter begins the new line.
- Tavern testing shows that leading ASCII spaces in common-message records are also
  consumed layout bytes. The rebuilder now preserves the original leading-space count
  automatically, and both aligned and plain English line breaks emit `0A 20`.
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
