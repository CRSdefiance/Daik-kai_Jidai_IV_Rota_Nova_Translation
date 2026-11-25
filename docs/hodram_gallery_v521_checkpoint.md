# V521: original Hodram Gallery display verification

The user authorized isolated testing cheats. A copied DeSmuME battery save sets
only the low four system bits controlling Gallery availability and updates their
original signed-byte checksum. All six route-save slots and the original donor
remain byte-identical. V518 ROM/patch bytes remain unchanged.

The first temporary RAM-only attempt was overwritten by the game's system-data
reload when opening Gallery. It is excluded from unlocked-screen credit. The
persistent copied-save fixture passes original checksum routine020EEC50, summing
signed bytes at system-block offsets8 through0x43. It changes only the system
flags at cartridge0x3C03C and checksum at0x3C004. The original Gallery menu then
loads normally and shows Items, Ruins, Characters and Event Scenes; all four
complete foreground and blank-cell masks pass inside the original popup.

Original Event Scenes is an image carousel, distinct from ending movie playback.
Normal controls select Hodram and visit every41 positions. Each top-screen image
matches all49,152 pixels of its current ROM PXL, after native five-bit color
conversion. Every English caption matches complete five-pixel tracking glyphs,
including initial/final letters and blank cells. Captions are reviewed against
original Japanese in the proof. Relocated strings are read from actual runtime
RAM, including the Moonlight/Rafael, Camille/Hodram and Ironclad captions.

The two previously registered English-caption centering/tracking instructions
remain retained; all other tested scene-reader/centering code and image-table
bytes match the original. Carousel wrap returns the identical first image and
caption. The surrounding screen is exact except the original navigation arrows,
which become visible after the first carousel input.

Preparation: `scripts/prepare_gallery_save_v521.py`.
Verifier: `scripts/verify_gallery_hodram_v521.py`.
Proof: `work/analysis/gallery_v521/hodram_gallery_proof.json`.
Fixture manifest: `work/analysis/gallery_v521/save_fixture_manifest.json`.
Targeted Ruff passes. Forty-one labeled scene captures, popup, report, proof and
fixture manifest are archived at
`E:/Rota Nova translations/Screenshots/Test fixtures/gallery_v521`.
The normal-play guide archiver rejects synthetic Gallery captures.

This proves original Gallery display under authorized synthetic unlock flags.
It does not prove earned completion, normal ending triggers, movie playback,
other captains' galleries, hardware behavior or a complete playthrough. V518
remains experimental; no canonical promotion or new ROM build. All22 original
requirements and all18 incomplete plaques remain under audit. The full graphics
goal remains active. Revisit older record-based checks at full completion.
