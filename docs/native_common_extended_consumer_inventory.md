# Extended COMMON consumer inventory

## Current result

### V159 connected crew-duty consumers

The formerly unknown ship role virtual is now mapped to `020132C0`, which reads
`ship+1E+matched duty position`. 160 connected cases execute the two complete
native callers, actual duty/ship lookup, ordinary route tables, special roles
12/16, no-assignment/null-ship returns and native COMMON copying with intact
text/guards/stack/R4–R11. Eight tests and Ruff pass. Current-route and assignment
values remain controlled inputs; live exclusion of null roles 9–11 and global
producer bounds remain unproved. No remaining-245 overlap is found in this
scope, and no unused-text or display-layout claim follows. See
[connected V159 evidence](connected_role_common_consumers_v159.md).

### V155 sound-path preservation refresh

Current saved V155 passes 152 native BGM update cases and 38 actual COMMON
title lookups with ARM946 copy alignment modeled. All 76 native title raster
cases match the previously reviewed V143 geometry/pixels exactly; all 38 titles
were visually inspected. The earlier longest-title clipping concern below was
resolved by the V143 native layout proof and remains cleared in V155. Five-pixel
tracking fits complete wording within 128 pixels. This adds preservation evidence,
not new translation credit or full physical Sound Setup verification. Current
durable evidence: `translations/bgm_title_native_layout_evidence_v155.json`;
current selector proof: `work/analysis/native_sound_selector_bounds_v155_proof.json`.

### Additional four-route selector and numeric leads

`inventory_current_route_common_tables.py` maps native selector `02053C6C`
and previously unlisted varargs wrapper `02053BD8`. The wrapper passes saved
incoming r0 to that selector and then the returned ID to `0205528C`.
The selector reads the current-route index through real `0207F244`; if its
primary slot is FFFFFFFF it searches four fallback slots. It contains no
primary-index clamp. This is distinct from the eight-slot actor selector.

The source-pinned main ARM9 direct-BL inventory finds 36 wrapper callers and
five direct selector callers. Thirty-five wrapper table addresses resolve
locally. The remaining wrapper caller `020DB080` uses fp, loaded from literal
`020DB124` before intervening conditionals/calls; its table `02116690` holds
IDs 3328–3331. Two direct selector producers have seven reviewed branch table
alternatives at `02012478` and `020125E0`. Their tables cover IDs 1789–1870
in separate four-entry groups. All reviewed/local tables execute the actual
selector and getter for route fixtures 0–3: **172 cases**, including real
sentinel fallback paths. None of those table slots selects IDs 3289–3319 or
3393–3606. Cases repeat some tables across callers; this is not 172 unique
messages or complete consumer/display approval.

Two direct paths at `0201276C` and `02012900` still obtain table pointers
through indexed arrays after `02081F54`. The exact source regions are now
mapped separately: `02130BDC`–`02130C30` and `02130B88`–`02130BDC`, 21 words
each, ending at adjacent pointer groups. Each has 16 nonnull pointers and five
nulls. The 32 nonnull four-route tables contain crew-assignment dialogue;
128 additional cases execute the actual array loads and native selector up to
the following COMMON accessor. Their slots do not select the remaining 245 IDs.
The 21-word extent is a reviewed static region, **not a live index bound**.
The callers handle indexes 12/16 separately and return early for 24, but null
indexes 9–11 have no corresponding local guard. They are not executed as valid
fixtures or silently omitted from the evidence. A changed indexed load is
rejected by the saved verifier.

Upstream `020820DC` searches 31 bytes at input object+6, returning the matched
position or sentinel 32. `02081F54` then resolves a ship object through
`02082E04`/`02036C94` and calls its vtable+18 method with the matched position;
no-match or null ship returns 24. The ship resolver uses a stored byte and
native 140-byte object stride, with 155 as null sentinel. The real virtual
method, constructor/type dispatch, live role-index range and exclusion of
9–11 remain unproved. This mapped chain cannot yet establish global bounds.
The fifth direct selector call is the wrapper's incoming argument.
Indirect callers, loaded sections/overlays beyond serialized ARM9 direct BL,
live route writers, gameplay reachability and outer presentation remain open.
Evidence: `work/analysis/current_route_common_tables_clean.json`.

`inventory_remaining_common_numeric_references.py` separately inventories all
aligned halfword/word numeric matches in loaded ARM9 sections and decompressed
overlays: 2,039 matches, including 66 full words. These are **numeric leads**,
not a remaining-text count. Exact native constructor spans show three referenced
halfword matches are low halves of full function pointers: `0213FF38` contains
`02050D58`, `021400C4` contains `02050D84`, and `021446E4` contains `02060DCC`.
They are not scene IDs 3416, 3460 or 3532. Literal `0205A16C` is the existing
3316-byte stack-restoration size; its actual loads/add-to-sp/returns are pinned.
A changed stack-restoration producer is rejected by the saved verifier.
Other numeric leads remain unclassified, including geometry-like halfwords
at `0214532C`. Literal-address matches alone do not prove dereferencing.
Evidence: `work/analysis/remaining_common_numeric_references_clean.json`.

Both scripts pass Ruff; current-route research now has 172 selector-only cases
and 128 connected indexed-caller cases. No ROM, English manuscript, formatting gate,
release registry, candidate or canonical baseline changed in this research.

The exact clean-ROM scan now includes ARM direct tails, locally resolved BX/BLX
targets, potential Thumb BL/BLX pairs, and MainCodeFile auto-load sections at their
actual runtime addresses, as well as overlays. This produces 619 candidates,
including three register tails. It is an inventory of possible references;
function/data boundaries, external predecessors and gameplay reachability are
not established by scanning instruction-shaped bytes.

Evidence: `work/analysis/native_common_extended_calls_clean.json`.
Reproduce with `python scripts/inventory_native_common_extended_calls.py` using
the bundled dependencies. Twenty-two focused existing/new tests and Ruff pass.
No ROM, translation, formatting approval or release profile changed.

## Two individually reviewed producers

- Caller 020BE534 is guarded by signed comparisons requiring input r6 in 21–144.
  It subtracts 21 into r1 before calling 020BF328. That wrapper adds 137 into r0
  and tails through literal 020546B8. Thus this guarded path selects native IDs
  137–260. It does not intersect promotional IDs 3289–3319 or remaining scene
  copies 3393–3606. This conclusion is scoped to the reviewed caller.
- Tail 020590F8 forwards to varargs wrapper 02053FE4 through a literal. Its eighteen visible
  assignment blocks select 1003–1019 and fallback 998, with multiple branches
  joining at 020590F0. These are ordinary shared conversation messages. Selector
  paths and incoming callers still need separate review; no gameplay-reachability
  or exclusive global range claim is made.

The report saves source-ROM/component hashes, exact reviewed code-span hashes,
and each switch assignment's original Japanese. The whole clean ROM is pinned
before extraction; the switch tail literal is checked explicitly.

## Branch-join correction

The previous linear-window propagation could report 998 at the switch tail by
reading only the final assignment before the join. The extended scanner now
discards values from before any visible incoming branch target. It still resolves
the literal target loaded after that join, but reports the message argument as
unknown. Tests cover that case, a fresh assignment after a join, direct tails,
the wrapper addend, resolved/unknown register tails, and Thumb call decoding.

External predecessors outside the window remain a limitation. Zero resolved
promotional/scene references is not evidence that those copies are unused.

## Actor-variant table wrappers

Two additional wrappers, 02053EC0 and 02053F0C, pass incoming r1 as a table
pointer to selector 02053F4C, then pass its returned native ID to 0205528C.
Their 92 call sites are separate from direct native-ID arguments: 89 table
pointers resolve locally, and all 89 contain valid native IDs or FFFFFFFF
sentinels in the eight slots read by the selector's fallback loop. Three incoming
table pointers remain unresolved by the short-window scan. Individual longer-span
reviews now resolve those three calls as five table alternatives: 021189C0 at
0202DE94, 02118980/021189A0 at 02030B10, and 021170E0/02117160 at 02033E7C.
Their complete fallback slots and exact producer hashes are saved in the report.
They contain tribute notices, blizzard/storm warnings, and defeat/succession
messages. None of these resolved fallback selections
intersects the remaining promotional or scene-label ranges.

The primary index comes from 0207E988, which reads a byte at character-source+1C
through 0207EB24. The chain 7EB24 -> 7EE08 -> 7F1F4 resolves the character index;
CDAB4 then selects immutable source table 02120B80 + index * 32. The special
player path uses 7F244's current-character index. It has no local clamp. Therefore eight fallback slots do not
prove the complete range of primary selections: valid character-index producers
and virtual type dispatch remain to be bounded. The report includes exact wrapper/selector/getter hashes.
Tests ensure pointers cannot be counted as message IDs, retain sentinel and
source text, and reject misaligned/out-of-bounds tables and invalid IDs.

Four other unresolved calls at 0210338C/021033E4/0210342C/0210346C read the
already documented treasure-map clue tables (IDs 3607–3657). The corresponding
manuscript is `common_b39_treasure_clues_manuscript_v2.json`. Those callers do not
select the remaining scene-label range; their actual index-field bounds still
need individual verification. A numeric value matching promotional ID 3316 at
clean offset 5A16C is a stack-restoration size loaded into ip and added to sp,
not a text selection. Numeric matches alone must not classify a text consumer.

Reviewing the actual V140 selections from the newly resolved blizzard table
revealed placeholder fragments at 389–391. V141 repairs those messages with
source-faithful English, full-owner repacking and strict release gates. This
consumer mapping produced an actual translation correction; see
`all_routes_unified_v141_checkpoint.md`.

## Next work

## Additional bounded BGM producer (V143)

Dynamic accessor call `02109274` uses base native ID 3249 plus object field +108.
The reviewed BGM constructor initializes that field to 2. Native update segment
`02108FC0`–`02108FE0` wraps its value within 2–39; 152 actual update cases pass.
Thirty-eight actual warm-cache calls execute the selector and COMMON accessor
against V143's true reblocked owners, preserving every full English title at
IDs 3251–3288. This reviewed producer does not select promotional IDs 3289–3319.
Four focused tests pass, including a changed wrap that would reach promotional
ID 3289. This is not an exclusive global-writer or unused-text proof.

The adjacent SFX class also writes +108, but its audio lookup values 0–72 must not
be combined with the BGM ID base. Its caption renderer at `02108EC0` indexes a
separate pointer table with +10C. Field offsets alone cannot establish class
ownership. Evidence: `work/analysis/native_sound_selector_bounds_proof.json`.
The longest BGM title has 23 characters; actual centering/clipping in its 128-pixel
panel remains a presentation risk to check. No ROM or registry changed.

Trace unresolved incoming IDs and table/script producers into the COMMON accessor,
starting with dynamic callers near the Online/promotional constructor paths.
The 31 full promotional localizations remain authored but have no approved native
display layout. The 214 scene/artwork/name selections still require separate
consumer classification despite matching already translated caption families.
