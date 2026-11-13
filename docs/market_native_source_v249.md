# Market native source and read-only runtime state V249

Previous goal turn: progress on complete market icon composition and the user's
continuing plaque-audit requirement. Current turn: market-specific crop logic,
complete active source/cache identity and a bounded CPU/TCM export reader.
V249 is research evidence. V247 remains the unchanged registered candidate.

## Original Market method replaces the cargo-only attribution

The Deal title's native constructor calls `020C37B0`. That method iterates the
five local-goods slots. It calls original getters `020BCB80` (occupied),
`020BCC1C` (goods ID), and `020BCC04` (indicator type), then creates the goods
source view through `02047978`. The indicator constructor is
`020C3A38..020C3A80`, using `(type-1)*8+80`, y216,8×8 and palette bank9.

Five bounded original-code cases verify all types1–5, their source coordinates,
complete view extents, palette halfword and surrounding32 guard bytes. Resource
registration/cache allocation and complete frame loading run through the original
native helper with only SDK filesystem bridging. The original market/getter code
matches clean byte-for-byte. The caller's type/stack context is supplied for the
fragment; this is not an execution trace proving when the live game dispatched
that particular indicator construction.

## Same-frame CPU/TCM source verification

The optional `--dump-native-state` capture flag invokes serialization only for a
read-only export. It never calls the load/unserialize API. A new fresh market boot
uses the same normal inputs. All43 captured PNGs are byte-identical to V248.
Serialized main RAM equals the direct RAM export and remains unchanged afterwards.
No savestate is loaded and no memory is injected into the emulator.

The reader follows the pinned core's native version12 header, chunk extents and
four-character tags. It checks complete chunk boundaries, terminators, duplicate
region names, compressed extents and declared field lengths. Five parser tests
cover compressed/uncompressed identity, duplicate-region rejection and truncated
exports. CPU registers,32KiB ITCM,16KiB DTCM, extra RAM, IO and OAM are exported
with pinned hashes. DTCM maps at027E0000; the extra RAM region is zero.

At the observed render phase, the ARM9 instruction address is `01FFAFB0`, while
its pipelined R15 is `01FFAFB8`. The actual code shifts the source pixel nibble.
R5 points to frame pixels at `02320CA4`; R6 points to bank9 at `02320364`.
The inferred complete header at `02320230` matches all35,444 original current-ROM
frame bytes, including every header, palette and pixel byte. The live source
rectangle is `(0,224,32,32)`: a general frame tile, not one of the indicators.
This establishes active use of the correct resource/bank at that phase; it does
not convert this observation into a trace of the4/5 indicator draw.

A candidate Trading View table occurrence was investigated. Its candidate slot
getter results do not match the visible goods, so those results are explicitly
rejected as active-model proof. A class-table occurrence by itself is insufficient
to establish active dispatch. The diagnostic JSON is labelled accordingly.

## Remaining scope

Exact live indicator dispatch, its gameplay meaning and quantity arithmetic remain
open. V248's full five-icon/130-indicator-ink pixel proof remains valid and separate.
All17 redesigned plaques and Equipped Items remain explicitly incomplete in both
audits. The four Online sources, eleven unresolved legacy blocks, broader native/
embedded/environmental coverage and final whole-goal review remain open.
No ROM, patch, production renderer or release-stack bytes change this turn.
The full graphics goal remains active.

## Evidence

- `scripts/verify_market_native_v249.py` and `work/analysis/market_indicator_v249/proof.json`.
- `scripts/inspect_desmume_state_v249.py` and `tests/test_native_state_export.py`.
- `scripts/headless_desmume_v193.py`: opt-in native-state export; default flow unchanged.
- `work/emulation_v193/market_native_v249/capture_report.json` and `native_state/`.
- Pinned official source identity: `work/analysis/market_indicator_v249/source_identity.json`.
  The state layout comes from [the pinned DeSmuME source](https://github.com/libretro/desmume/blob/95b4d798731caa809125b6c3c11d17cc332ff6ef/desmume/src/saves.cpp).
