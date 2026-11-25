# V562: original month/day graphic consumer

The current experimental ROM remains V558, SHA256
bf62f246f485c7adf9a763c7765bc63476128f73f6cce983717bf297877cff6d.
No graphics, executable code, registered layers, ROM or patch changed.

## Original code and actual resource

The original ARM9 call at 020B97AC constructs a frame view with source rectangle
[104,112,136,128], palette parameter 9. Its owner literal at 020B979C resolves to
02313F60, the frame resource. This original constructor region is byte-identical
in the current ROM. Both authored date cells fit completely within this crop:
M [104,116,110,124] and D [128,116,133,124]. These localize 月 and 日 as compact
month/day initials; this work retains the existing lettering.

Three initially similar code leads at 02007130, 0200DFDC and 0200E00C instead
resolve to marker owner 02313F74. They are rejected as evidence for these frame
date cells. Coordinates alone do not establish resource identity.

The prior V561 census searched exact miniature cell origins. A broader view
search finds actual date view 02192140 in the earlier Common wheel and Swap Ships
snapshots. Those hidden/inactive occurrences do not earn visible lettering credit.

## Ordinary visible checks

A fresh headless DeSmuME boot of V558 loads an isolated byte-exact copy of the
existing Syracuse gameplay save. No savestate, location/inventory/condition fixture
or cheat is used. The source save remains unchanged. Actual navigation reaches:

- Frame3200: Syracuse town, date visibly reads 6M12D.
- Frame3500: Port submenu, same date display.
- Frame4300: Sail submenu, same date display.
- Frame4700: ordinary departure/Sea View; a separate numeric date display is
  visible. It is not credited as another use of the M/D artwork.

For all three credited frames, original routine 020D4170 resolves actual view
02192140 to a resident byte-exact `/_pxl/__frame.pxl`, at 0232D330 in this boot.
The address differs from earlier boots; the verifier resolves and compares it
rather than requiring a fixed heap address. The full 32x16 source crop contains
only zero and 34 white ink points. Palette bank9/index9 is original white.

Both complete glyph cells match uniquely at destination M (122,333), D (146,333).
All102 visible ink points and264 complete-cell ink/blank pattern points pass
across six glyph appearances. There is no dropped first/final stroke or cropping
of either cell in these contexts. Numeric date arithmetic, the intervening number
glyphs, transparency outside the two cells, the full512-pixel composite and other
date renderers are not covered by this check.

## Evidence and remaining work

- `scripts/verify_date_consumer_v562.py` reproduces mapped-code/resource checks
  and the bounded native framebuffer comparisons.
- `work/analysis/action_consumers_v562/date_native_proof.json` records hashes,
  view fields, source rectangles, destinations and the exact capture report.
- `E:/Rota Nova translations/Generated/work/emulation_v193/action_consumers_v562_navigation`
  contains the ordinary run, input schedule, PNGs and read-only RAM exports.
- An unchanged ordinary screenshot and provenance are saved under
  `E:/Rota Nova translations/Screenshots/Guide candidates/V558 Date display`.
  Guide publication remains unapproved.

The other five miniature captions—Done, Rank, Cancel, Pick Cargo and Pick Ship—
still need actual native consumer/crop checks. The global plaque texture defect
and all18 original plaque/hint entries remain open. All22 historical requirements
retain their full scope. This targeted emulator evidence is not a complete route
playthrough or physical-device test. The graphics goal remains active.
