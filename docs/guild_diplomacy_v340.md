# Guild diplomacy captions and actual mystery-map fragment V340

## Source-faithful menu correction

A normal V338 cold boot from an isolated older cartridge save reaches Stockholm's
Guild with the first-mate fleet context. A third Guild command remains Japanese.
Its source table reveals six related diplomacy commands, including entries hidden
in this save's observed menu. All seven source labels are now localized.

| Japanese | English | Reason |
| --- | --- | --- |
| 交渉文書の発送 | Send Documents | Dispatch negotiation documents through the Guild. |
| 親善交歓 | Goodwill | Friendly diplomatic exchange; no invented gift cost. |
| 協定締結 | Sign Pact | Form an agreement without assuming its exact treaty terms. |
| 協定破約 | Break Pact | End that agreement. |
| 停戦 | Truce | Cease hostilities. The label does not claim successful agreement. |
| 宣戦布告 | Declare War | Preserve the explicit declaration of war. |
| 威圧 | Threaten | Apply intimidating diplomatic pressure. |

Six labels fit their exact original allocations. Threaten needs nine bytes with
its terminator; its old slot is eight. The complete word is appended to the owned
pool and its one table pointer redirects there. Its original Japanese string is
retained. Existing pool bytes, menu logic, availability flags, icons, fonts,
palettes, routes and other components remain exact. Startup copy/cache coverage
and arena limits extend through the declared new payload.

The five-command V339 candidate was an intermediate audit build. Reviewing the
complete table found Truce and Threaten, so **V340 supersedes that partial build**.
No V339 candidate was promoted or handed off as the complete correction.

## Verification and remaining menu contexts

Fourteen native rasters cover all seven complete labels in both4-bit and16-bit
formats. The four-bit renderer clears a spare terminal half of its paired glyph
cell for odd text lengths. The independent reference includes that empty cell;
the executed text remains the actual unpadded command. The initial reference
mismatch concerned33 transparent bytes after the final letter, not missing ink.

Actual normal playback shows Send Documents twice and Goodwill/Declare War twice.
All179/101/130 respective ink pixels and every blank cell match the independent
native font. Nine comparable frames differ only in the popup-menu area;62 other
saved-game frames match exactly. The six-entry constructor retains its original
conditional availability rules. Sign Pact, Break Pact, Truce and Threaten remain
unavailable in this save and their actual displays stay open. Their source-lock,
complete native rasters and storage safety pass; no synthetic eligibility or
unlock was used.

The fresh31200-frame New Game run matches all81 comparable V338 frames, including
title, selection, opening, town and sailing. Both emulator processes terminate
normally without callback errors. Complete V338 reproduces byte-exact, all470
batches and prior stages/records are preserved, and only ARM9 changes.
The clean-input patch reconstructs V340 exactly. Startup/cache/ARM7/arena and
focused Ruff checks pass. The canonical baseline remains unchanged.

## Actual Ancient Map fragment

Ordinary inputs purchase Gem-Eating Gem Map1 for3000 coins and inspect Ancient Map.
The visible name becomes Gem-Eating Gem and an acquired fragment icon appears.
Selecting that row displays a map fragment. Every one of its **11880 nonzero source
pixels** matches `/_pxl/mysterymap/10_1.pxl` at actual origin(8,18), native240x157.
The whole resource is source-exact and has no separate Japanese caption. Retain
this cartographic artwork.

An initial comparison against the regional `seamap.pxl` atlas finds no match.
The actual painting is a different mystery-map resource. This does not verify any
regional atlas page, legacy304x200 archive use, all other fragments, or full
transparency/blending semantics. Those requirements remain open.

The original cartridge save remains unchanged. Its earlier progression provenance
is unknown. Only the isolated copy is used, with normal controls, no savestate,
RAM injection, save editing or unlock changes. This is targeted automated emulator
verification, not a completed route or physical-device test.

## Integrated experimental candidate

| Artifact | Identity |
| --- | --- |
| ROM | `out\all_routes_combined_v340_candidate.nds` |
| ROM SHA256 | `bf8a5a76fead7fa20eac3c262799f0d29b14b66131a6ab61978cbdfb6f1848c9` |
| Patch | `out\all_routes_combined_v340_candidate.xdelta` |
| Patch SHA256 | `e287d33aa0ef26ab0ad8bd37a31d12db9646ce786fc070fa2addbf4e6f55db06` |
| Profile | `all-routes-unified-v340` |
| Canonical base | `out\raphael_natural_v2_accepted_base.nds` |
| Base SHA256 | `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe` |

Both graphics audits, progress documents and requirements ledger are updated.
All18 plaques/hints and Weapon/Armor variants remain incomplete. Low-resolution
Online images remain user-exempt. Other map, legacy, Gallery, ending and gameplay
requirements remain open. At actual full-goal completion, revisit older record-based
checks. The observed Guild wording "Letter job" and earlier clue word splits belong
to that older prose review; this menu-label correction does not certify them.

Evidence: `work/analysis/guild_diplomacy_v340/release_proof.json`, `native_proof.json`,
`startup_proof.json`, source/actual mystery-fragment comparisons under
`work/analysis/regional_maps_v339`, and both V340 capture reports.
Verifier: `scripts/verify_guild_diplomacy_v340.py --live`.
