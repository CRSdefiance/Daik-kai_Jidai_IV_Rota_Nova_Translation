# Legacy archive access and current native registry V384

Evidence checkpoint on unchanged V383. No ROM, patch or graphic was changed.
The graphics goal remains active, with all 22 historical requirements and all 18
incomplete plaque/hint entries retained.

## Actual save availability

The read-only RAM exports from the genuine older-save checks V379, V380 and V381
all have system halfword `0227985C` equal to zero. The original Gallery predicates
therefore leave Characters and Event Scenes unavailable in those observed states.
This does not establish the donor save's entire history or say those views can never
be unlocked. It supplies no deep Gallery artwork display credit.

## Expanded filesystem and archive census

`scripts/map_legacy_archive_access_v384.py` scans all five current ARM9 main-code
sections and the declared ARM9 overlay for direct aligned ARM BL, direct Thumb
BL/BLX and aligned function pointers to native archive open `020D2018`, archive
block read `020D1EF0`, and SDK filesystem open `020DED50`. It records 39 direct
calls and zero aligned function-pointer candidates, with nearby instruction and
string-literal evidence. A nearby literal is not treated as proven argument dataflow.

Resource-stem searches include case variants and file names without assuming the
`.DK4` extension. They expose CMMNIMG.000, SLACKIMG.DK4 and initialized loose SLACK
filenames, rather than an additional CMMNIMG.DK4 or WINFRAME filename. This is bounded
static evidence, not a global unused-file claim.

The archive-open call at `02024170` takes its filename from table `02134580`, indexed
by the original route field. Its four valid route entries select SC0, SC1, SC2 and
SC3. `scripts/verify_route_archive_dispatch_v384.py` executes the original routine
and archive readers for block zero of each route, bridging only SDK file operations.
All four complete loaded blocks, object/neighbor guards, stack and saved registers
pass. Four immediate cache hits preserve all object bytes, do no additional file I/O
and return the original success value one. No handle remains open.

The valid route indices, block zero, owner buffer and global field are supplied
isolated native contracts, not live-game mutations or proof of every route state.
The test initially assumed case-sensitive ROM paths and a zero cache-hit return;
both were corrected from the exact paths and original instructions. No ROM changed.
This dynamic archive path is now identified as route-script loading, narrowing the
unresolved graphics-consumer search.

## Current initialized PXL owners

`scripts/census_native_image_registry_v384.py` executes the unchanged primary and
Online resource initializers. In RAM bounds `02300000..02400000`, the known original
PXL owner class (`02160538`) yields 362 initialized owners. Their exact filename
pointers/fields are recorded. Of these, 347 distinct filenames match real ROM PXL
files. Fifteen filename owners have no exact ROM-path match, and 313 of the 660 ROM
PXL files have no owner of this class in this tested initialization/bounds.

The unmatched owners include bare `/_pxl/Online06.pxl`-style names. Their active use,
possible aliases/replacement and later registration remain unknown. They are not
silently redirected to similarly named files and are not called confirmed defects.
The files without matching owners include event/ruin, logo and ship resources;
later registration and other owner classes must be traced. Existing title and
other actual display proofs remain valid in their recorded scope.

None of the observed owner filenames is a CMMNIMG, SLACKIMG or WINFRAME archive.
This establishes only this PXL owner class's inputs. Other classes, later dynamic
registrations, numeric file IDs, generic readers, generated paths, indirect calls
and actual gameplay/GPU consumers remain open. No archive is declared globally
unused, and the eleven unresolved legacy blocks remain in the storage census.

## Evidence and next work

All three new scripts pass targeted Ruff. Evidence is under
`work/analysis/legacy_archive_access_v384/`: `access_census.json`,
`route_archive_table.json`, `route_dispatch_proof.json` and `PXL_registry_proof.json`.
The candidate remains `out/all_routes_combined_v383_candidate.nds`, SHA-256
`2259d228e48f8294831d6aeceffbd32654b4502623513d51762387f7b0b512d2`.
Its exact patch and full handoff remain those of `docs/tavern_round_v383_checkpoint.md`.

Next consumer leads: caller-supplied file-open sites at `020B7178`, `020D0474` and
`02100348`, the cache reader's owner filename field, later dynamic PXL registrations,
and the unresolved bare Online owner references. Continue genuine occupied equipment,
alternate plaque states and available environmental/movie/Gallery display checks.
Low-resolution Online screenshot translation remains exempt by user instruction;
this filename investigation does not revoke that exemption.

No finalized screenshot was generated in this source/native checkpoint. Do not add
simulated or ambiguous views to the E drive guide archive. Revisit older record-based
checks when the full graphics goal is complete.
