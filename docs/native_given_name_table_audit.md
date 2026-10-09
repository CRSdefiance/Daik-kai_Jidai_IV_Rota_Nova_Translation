# Native given-name table audit: V147

## Current residual-name research after V149

Both remaining Japanese given names are translated as Vels and Akaboo, using
the established Raphael spelling and a documented phonetic project spelling.
All 207 startup-loaded ordinary getters preserve pointer identity and the other
205 names; no Japanese script remains in their given-name outputs. Four paired
rows and four fleet rasters preserve complete text and independent pixels.
Thirty focused tests and lint pass; V150 build/verification is underway.
Five inherited full-width Latin initials and older role fidelity remain open.
See `residual_character_names.md`. Earlier pending/root-cause entries below
are retained as research chronology.

## Startup BSS lifetime and two complete square-shopkeeper labels

The actual startup clear loop 0200088C–020008AC now executes after the real
autoload copier. Its full declared BSS interval becomes zero while loaded DTCM
name storage stays byte-exact. All 207 ordinary getter results survive this
ordering. This proves why serialized-file addresses are unsuitable for the moved
names: those addresses lie in the interval the SDK clears after copying.
Cache maintenance and full hardware/game initialization remain contracts.

The two remaining square-shopkeeper owners at 15D088/15D094 are localized as
**Square Shopkeeper**, retaining the original location and role. Their complete
identical Japanese allocations share 24 source-owned bytes; full English plus
NUL uses 18. Every-byte ARM9/overlay scanning finds exactly two start references,
with no interior/overlay references; both select the shared complete label.
Every other research ARM9 byte and all 205 other ordinary names remain exact.

Actual startup copying, BSS clearing and all 207 native constructor/index/getter
selections pass against this combined research. Two Japanese given names remain,
indices 61 and 77; they need established spelling/context review. Source/context/
localization/naturalness gates for the shopkeeper prose pass. Visible nameplate
layout, class/captain eligibility and formatting/integration remain pending.

Tool: `scripts/prepare_square_shopkeeper_names.py` (native checks and Ruff pass).
Draft: `translations/square_shopkeeper_names_manuscript_v1.json`.
Research: `work/analysis/square_shopkeeper_research_arm9.bin` and
`square_shopkeeper_native_proof.json`. V147 remains unchanged.

## Root cause and actual-loaded-storage research repair

The intact entity relocation pool from `entity_ship_names_arm9_v2.json` starts
at canonical file offset 1720A8, inside the 1,632-byte DTCM autoload section.
The V143 ITCM extension enlarged that preceding section by 652 bytes, moving
the entity pool to current file offset 172334. All 193 entity pointer fields
still contain their original intended file-address values. Those stale offsets
select unrelated item suffixes or ITCM bytes. Full inherited pool bytes and
pointer provenance are now checked exactly against the originating batch.

SDK directory ownership places this pool at actual runtime address **027E0248**,
independent of serialized file offsets. Research rebases all 193 affected entity,
speaker, nationality, place and ship pointer fields to their complete logical
string starts in that loaded section. Pool bytes, executable code and every
other ARM9 byte remain exact; nothing is appended, shortened or reallocated.

The actual startup copier 020009E0 loads the entire DTCM section, with native
directory iteration/loads/stores and only CP15 cache instructions contracted.
All 193 referenced complete English strings match after the copy. In that same
machine, all 207 ordinary constructor/index/getter cases return printable names;
the whole loaded section remains byte-exact after those consumers. This restores
the inherited role names that had become fragments. Four Japanese given-name
entries remain: 61, 77, 82 and 83. Native caller/class/captain eligibility, full
startup/BSS/hardware use and downstream display still need verification.

Tool: `scripts/probe_entity_name_runtime_rebase.py` (193 pointers, 207 native
getters and Ruff pass). Research ARM9/proof:
`work/analysis/entity_name_runtime_rebased_arm9.bin` and
`entity_name_runtime_rebase_proof.json`. No ROM/profile changes are made.
Next: verify runtime ownership and affected native display consumers, review
restored source-faithful wording, translate the four residual names, and prepare
strict integration. Other pointers into shifted autoload data also need auditing.

The fleet-name bounds investigation now executes the actual ordinary character
constructor and given-name getter for 207 source-table selections. The native
7F254 loop initializes 207 ordinary objects and a separate player interface;
this inspection range does not by itself establish valid fleet-captain IDs.

Chain: ordinary constructor 7EB3C writes vtable 148414; +20 accessor 7EB0C calls
7EB24 → 7EE08 → 7F1F4. Ordinary zero-type index calculation selects CDAB4's
immutable table 120B80+index*32 and returns its first pointer. Every inspected
current selection matches the actual getter output, with intact return/stack.
Constructor/type fixtures are explicit; player interface, live class assignment
and gameplay reachability remain open.

## Findings requiring repair/classification

- Indices 84–91 return nonprintable current payloads where clean Japanese says
  `広場の店主` (square shopkeeper). These eight results cannot be accepted as
  translated names. Native getter outputs are established; gameplay callers
  and the translation layer that displaced their original storage need tracing.
- Japanese remains at 61 (`ヴェルス`), 77 (`アカブー`), 82 and 83
  (`広場の店主`). Eight additional Japanese-looking results are the nonprintable
  payloads above; total Japanese-bearing results is 12, not 12 valid labels.
- Printable results can also violate source meaning: 109–112 (shipyard worker)
  currently return ` Shield`; 120–124 (guard) return `ec Pictorial Map`;
  126 (regional lord) returns `torial Map`; 128 (local king) returns
  `Sweeping Katzbalger`; 129 (magistrate) returns `tzbalger`; 130 (daimyo)
  returns `riander Stone Map`. Other affected role names continue beyond 130.
  Their current first bytes are printable, so encoding-only tests missed them.
- Some ordinary names already resolve correctly to complete English, such as
  Raphael, Hodram, Lil, Maria, Peralonso and William. Do not overwrite those
  from memory or use corrupted role results to infer captain-name bounds.

These are source/current static-name fidelity findings backed by actual getter
execution, not a claim that every index is reachable as a captain or a displayed
character. The full table must be classified and repaired from clean Japanese,
including relocated owner/reference coverage and all affected name consumers.
Checking only that a pointer lands on printable text is insufficient.

## Evidence and next work

Tool: `scripts/audit_native_given_name_table.py`; 207 actual selections and Ruff
pass. Proof: `work/analysis/native_given_name_table_v147_audit.json`, including
all source/current strings, pointer fields, original bytes, statuses and native
consumer locks. Pinned V147 ARM9 SHA-256:
`33dc6e6ac7ababb513a773647edd6f93cb5c08b19fad2500e7695f95d8629d75`.

Prior source-table/index caveats in `native_common_extended_consumer_inventory.md`
still apply. Next: classify all table roles and source-owned allocations, trace
displaced references to their translation layers, restore complete natural-English
role names and remaining proper names, then verify native getter/display output.
Fleet captain eligibility/setters and player virtual name behavior also remain
open. V147 is unchanged and experimental; do not promote while these defects
remain unresolved.
