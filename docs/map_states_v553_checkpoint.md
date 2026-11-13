# V553 observed World Map states and caption

The fixed frame36000 composition from V552 failed at three earlier frames.
The new verifier resolves those differences using each frame's actual masked
map bitmap, original icon crops/banks, and the game's ASCII font. No ROM,
patch, artwork, release registry, save, or translation is changed.

| Ordinary captured frame | Additional observed elements | Exact map pixels |
|---|---|---:|
|35400|Circular marker, blue selection outline, N. Sea caption|39040|
|35600|Circular marker, blue selection outline, N. Sea caption|39040|
|35800|Circular marker; indicator absent|39040|
|36000|Circular marker and 24x24 indicator|39040|

All156160 pixels pass with no exclusions. Each source overlay retains its
clean-ROM crop and palette. The two captions each match all66 font ink pixels,
including first and final glyphs. Deliberately removing either complete edge
glyph produces a mismatch and confirms the check detects their loss.

## Caption meaning and measured geometry

The clean-ROM literal at0214C79C reads 北海 (North Sea); its existing English
replacement is N. Sea. This is a faithful abbreviated geographic label.
The observed caption is a40x16 white region at123,248 with native6x11 font
ink at125,250, colour BGR555(0,1,0). A23x20 blue outline at123,229 overlaps
the caption's first row by23 pixels. These measured primitives reconstruct
the complete images. The original painter and its order have not been traced;
this composition does not claim to execute those producers.

## State evidence and limits

The actual indicator object's +70 word is1/1/0/1 in these four frames.
It correlates with absence at35800, but is also1 while the indicator is absent
in the two Sea Areas frames. It is therefore not a sufficient visibility
predicate by itself. An inspected original vtable slot02005D48 reads+1C,
not the hypothesized+10 subobject field. No original visibility getter is
credited as proven. Indicator presence is explicitly an observed-frame contract.

The source is the existing ordinary V546 cold-boot capture; no state loading,
preloaded battery save, cheats, synthetic RAM fixture, or diagnostic ROM is
used. This establishes these observed images, not all animation states,
complete route progression, or hardware behavior. Original mask creation,
caption/visibility producers, other banks/crops, sepia seamap and legacy CMMN
contexts remain open. All22 historical requirements and all18 incomplete
plaque/hint entries remain retained, including the global texture review.

## Evidence

- Verifier: `scripts/verify_map_states_v553.py`.
- Proof: `work/analysis/map_states_v553/observed_state_proof.json`.
- Existing component diagnostics and enlarged map crops in that folder.
- Ordinary capture: `E:/Rota Nova translations/Generated/work/emulation_v193/worldmap_source_v551`.

V546 remains current, SHA256
499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3.
The graphics goal remains active. The previous report-only turn verified that
the user's evidence was already saved byte-exact and all18 plaque entries
were still incomplete; it did not add a correction or advance a completion gate.
This turn adds complete four-frame evidence and the caption translation check.
