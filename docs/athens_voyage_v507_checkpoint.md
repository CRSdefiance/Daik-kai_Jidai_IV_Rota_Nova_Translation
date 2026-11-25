# Athens voyage and newly confirmed toast defect

Previous goal turn: progress on the current comic source review. This turn uses
normal gameplay in unchanged V502; no ROM/patch, inventory fixture, savestate,
teleport or unlock injection.

## Normal gameplay progress

An isolated copy of the genuine Istanbul save was cold-loaded. Ordinary inputs
complete Angelo's port event, resupply and depart, then steer to Athens. Original
city-coordinate getters and coastline queries only inform navigation; they never
write to the running game. A rat warning and exhausted supplies occur during the
approach. Normal docking, resupply and Save slot 6 complete in Athens. The run
stops normally at frame 25100. The original donor remains byte-identical.

The copied save is a useful Athens checkpoint. Inn recovery has **not** occurred,
and an independent cold reload remains to verify. No East Asian visit is credited.

All four Athens specialty labels match 365 exact native ink pixels and blank
cells: Olive Oil, Sultana, Artwork and Statues. The tiny third label was initially
misread as Armor; the original native commodity getter and exact font mask confirm
Artwork. First, internal and final letters are complete. This adds one normal city
context to the current stock renderer's evidence.

## Defect requiring repair

The Athens tavern's Myrine toast reveals an actual shared-dialogue defect in
native message **827**. Clean source:

> ふーん、%sさんね？ じゃ、お近づきのしるしに乾杯！

Current stored format: `Right...%s, right? A toast to our new friendship!`
The captured RAM contains the full expansion, including the `r` in `our`:
`Right...Hodram, right? A toast to our new friendship!`.

Frame 23300's exact 531-pixel native glyph masks prove the visible rows are:

```text
Right...Hodram, right? A toast to ou
 new friendship!
```

The split is at byte 36 and the following `r` is absent from the display. This is
a formatter/painter defect, not an absent byte in the translation. The inherited
portrait wrapper checks parent return `02054014` and selected IDs 801, 820/821 and
870–873; 827 falls through. The first row also uses x16 versus x22 for the second.

Next: repair the shared ordinary portrait-paragraph policy after substitutions;
verify whole words, first/last glyphs, guard phase, bounds and ABI across the
eligible message family. Review the toast's missing space after its ellipsis
against the clean source. Preserve explicit controls and other renderer formats.
Do not claim a global repair from a shortened line or a one-message screenshot.

## Evidence and limits

- `work/analysis/environment_voyage_v507/voyage_proof.json`.
- `work/emulation_v193/environment_voyage_v507/capture_report.json`, with all inputs,
  screenshots and read-only snapshots.
- `scripts/verify_athens_voyage_v507.py`: source/current message mapping, all capture
  hashes, original donor hash, specialty masks and exact dropped-character proof.
- `work/analysis/environment_voyage_v507/athens_route/water_route_proof.json`:
  original isolated coastline queries; point samples do not prove whole segments.

V502 remains experimental and now has a confirmed unresolved dialogue defect.
No repair candidate has been built. All 22 graphics requirements and all 18
incomplete plaque entries remain in the audit. Goal remains active.
