# Sky source geometry and retain review V208

2026-10-07. The previous goal turn made progress by verifying complete native
sky-record reads and retained facility labels. This turn resolves the regular sky
texture format and supplies complete source-art reviews. **V205 remains unchanged.**

## Correct source layout

The unchanged native fragment at `0206B0F8..0206B11C` writes matrix mode 2,
texture command `71531E00` to `040004A8`, and palette command `80` to
`040004AC`. The preceding matrix-register pointer is supplied explicitly from
its original literal; texture and palette commands are loaded by native code.
This verifies register-command production, not hardware projection or GPU rendering.

The texture command specifies **256×32, 256 palette entries**, with texture
byte offset `F000` and palette byte offset `800`. These dimensions cover each
regular 8,192-byte sky payload exactly. Source indices are linear texture pixels,
so the earlier eight-by-eight tiled diagnostics were the wrong source layout.
The register identities and texture fields are checked against the primary
[libnds video definitions](https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/video.h)
and [texture definitions](https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/videoGL.h).

All fourteen native-loaded payloads were rendered again with their own original
256-entry palettes. Every PNG preserves all indices and decoded RGB pixels,
including image edges; no interpolation or palette substitution is applied.
Together these views cover all **122,880 source indices** and all fourteen palettes.

Records 0–12 have the verified 256×32 extent. Record 13 has twice the payload and
is reviewed as a complete 256×64 source buffer. That buffer contains all source
indices, but the extra lower 32 rows' actual sampling is still unproved. A different
256×128 texture constant elsewhere in the ROM is not assigned to this record
merely because its address happens to resemble the sky texture address.

## Visual decision

All fourteen complete source views were reviewed at native resolution. They show
clouds, sun/moon, night, sunset, rain/light effects and green atmospheric imagery.
No readable Japanese label or other composed text is present in these source
views. **Retain every sky record unchanged.** These environmental images need
no invented caption or replacement lettering. Their palettes and source dimensions
are preserved; this decision is distinct from pending scene sampling/crop evidence.

Machine-readable decision: `translations/raw_environment_graphics_decisions_v208.json`.

## Normal sailing evidence and limits

The unchanged registered V205 candidate cold-boots through New Game, town and
ordinary sailing using controller input. Its final frame 19500 and read-only
4 MiB ARM9 RAM snapshot are hash-pinned. The actual getter at CB1B4 points to
`022CFD54`; the current environment selector at +C is **3** in this snapshot.
The final Sea View frame was visually reviewed. This overhead sailing view does
not expose the complete sky strip, so it is not substituted for exact projected
sky pixels or first/last texture columns. Scene projection, depth/crops and the
exceptional source buffer's extra sampling remain open where evidence is available.

Verifier: `scripts/verify_sky_texture_geometry_v208.py` (Ruff passing).
Proof and all source PNGs: `work/analysis/sky_texture_geometry_v208/`.
Cold-boot capture: `work/emulation_v193/raw_graphics_v208/normal_sailing/`.

No ROM or patch changed; no candidate was promoted. The full goal still includes
four Online screenshot bodies, other raw resources and unresolved embedded blocks,
name/artwork consistency, remaining native/gameplay verification and one complete
registered combined ROM with an exact reconstructable patch.
