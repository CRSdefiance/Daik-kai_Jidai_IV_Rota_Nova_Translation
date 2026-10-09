# V189 scoped native Online loader and cache verification

2026-10-05. The graphics goal remains active/incomplete. This research extends the
actual page-selection proof from [V189](all_routes_unified_v189_checkpoint.md).
It changes no ROM resource, release profile, translation batch or patch.

## Exact source and candidate

- Candidate: `out\all_routes_combined_v189_candidate.nds`
- Candidate SHA-256: `0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74`
- Candidate ARM9 SHA-256: `642177fcd6f6c0ef69c7cf7d89563c9a974183ab00223733016c814c5d8c74cf`
- Clean ARM9 SHA-256: `0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731`
- Page registration evidence: `work/analysis/online_resource_pages_v189.json`
- Probe: `scripts/research_online_loader_v190.py` (research version, not a V190 ROM)
- Saved results: `work\analysis\online_loader_v190_research.json`

Registration/cache/image-resolver code ranges are checked byte-exact to clean.
Native constructors are invoked individually: `0x0210E190` (2,864 distinct
instructions, resource registry/cache sentinel), `0x02111A90` (449, Online registry),
and `0x020D6C0C` (24 distinct instructions, native memory-pool initialization).
The real startup literal at ARM9 offset `0x5D24` identifies manager `0x0231272C`.
The pool is `[0x02313FF0, 0x02373FF0)`, exactly 384 KiB. No fabricated resource
owner, filename table, cache ID or loaded image pointer is injected.

## What executes and what is bridged

Each image view executes `0x020D3D30` with its real owner from the game's actual
page table and full 256x192 extent at origin zero. Resolver `0x020D4170` follows
file-mode 4 to the owner's actual virtual method `0x020D6558`. That code moves the
real LRU list, opens its registered filename, allocates from the native pool,
reads/closes the file, assigns the cache ID and resolves it through `0x020D68F0`.
All those operations execute original ARM code except the three SDK I/O boundaries:

| SDK boundary | Explicit harness behavior |
| --- | --- |
| `0x020DED50` open | Resolve the actual registered filename through the exact candidate ROM filesystem; provide FSFile start/end and byte count. |
| `0x020DEBDC` read | Copy that complete candidate file into the native-allocated pool destination; reject wrong byte count or escaped pool bounds. |
| `0x020DED08` close | Close the harness handle and verify no handle remains open. |

The SDK file-object initializer `0x020DF0A0` still executes natively. Resource
allocation, cache IDs, LRU updates, eviction, pool compaction and its byte-copy
routine `0x020D7650` are not replaced. The first 100,000/1,000,000-instruction probe
budgets stopped during a legitimate pool-compaction byte-copy. A local bounded
4,000,000-instruction call permits completion, with strict return/stack/callee-saved
register checks. No production code or shared probe helper was changed.

## Results

- All **23** real page screenshots participate.
- **27** cold/native resolutions; each complete file, palette/header
  and text pixel is byte-exact after native resolution.
- **27** immediately repeated hot lookups return the same complete
  image without extra SDK I/O.
- **20** resolutions execute
  native eviction because the image set exceeds the actual 384 KiB pool.
- **168** additional byte-exact checks validate all other
  still-resident registered images after each lookup/compaction. These use their
  real owner cache IDs and native lookup, without altering LRU order.
- All image view owners/extents/canaries and saved-register/stack ABI checks pass.
- All bridge handles are closed. Ruff passes for the source probe.

The four unfinished screenshots Online24/27/31/33 are tested first, then all 23
screenshots exercise the cache/eviction paths. This verifies source storage reaches
native resource views intact, including the newly authored header pixels and earlier
Online27 bubbles. The native `0x020D3A1C` routine is a view-field copier; it is not
used as evidence of a PXL parser or automatic sizing.

## Limits and next requirements

This probe does **not** verify NitroFS hardware, OS scheduling, full viewer
navigation, native pixel decoding, GPU layers/palette/color-key/alpha composition,
physical input, small-letter readability or complete gameplay. It cannot prove that
untranscribed screenshot dialogue/chat is faithful or localized. All four remaining
Online files, unclassified/contextual art and broad source/native/gameplay/final
acceptance requirements remain. V188 title work is retained in V189, still awaiting
cold-boot visual review. No candidate is promoted and no global graphics clearance
is claimed. Preserve the user's older record-based-check follow-up for eventual
full goal completion.
