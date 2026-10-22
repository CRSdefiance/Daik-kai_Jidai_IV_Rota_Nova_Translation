# V585: initialized resource tables and calculated-address candidates

Production remains experimental V581. No artwork, ROM, patch, profile or
canonical baseline changes in this batch. V584 is now recorded in all three
audits, four progress documents and its proof archive on E.

## Original initializer and resource publication

Executing original initializer0210E190 in current and clean machines gives the
same2,864 unique instruction addresses and1,898 nonstack writes. All executed
instruction words, owner values and filenames match clean source. It constructs
315 objects with the original PXL resource vtable02160538. Every object has its
two intrusive-list pointers linked to itself, a filename and unloaded ID-1.

For frame owner02313F60 and Confirm owner023139C0, the only nonstack initializer
writes containing a pointer into their20-byte object are the two self links.
The initializer does not place either owner in a filename/selection lookup table.
This is an initializer write trace, not a whole-program escape proof.

Two original cached-getter executions separately prove how list admission works.
The original020D6558 getter executes unlink020D66E8 and insert020D6704; the original
list head is02312734. Frame is admitted first, then Confirm, producing the expected
forward/back links. Original unlink restores Confirm's self links and the remaining
Frame list. Current and clean code/observations are exact, with complete call ABI.
Only the final cache-ID lookup is bridged to an explicit supplied header. The
header is not evidence that Confirm was loaded or drawn; file-loading paths are
asserted absent in these cached cases. No new ordinary UI or GPU credit follows.

## Stored pointers versus direct instructions

Every byte position of all loaded main sections and the declared overlay is
scanned for stored absolute pointers to the315 owners, including unaligned data.
ARM PC-relative load candidates are recorded separately. Executed initializer
literal locations are then separated from other stored references.

This distinction matters: many real resources have no direct non-initializer
PC-relative owner load because they are selected through pointer tables. Positive
controls find the stored table references for person16bit_00, mysterymap/10_1 and
title05. A diagnostic that calls every such resource 'initializer-only' from
PC-load counts is invalid and earns no display/non-use credit.

Thirty-five objects have no stored absolute base-owner pointer outside their
initializer literals. These include Confirm, title00/title01/title06, older window
frames, seamap, dia00/dia01 and shipback. Their complete list and all315 records
are in `owner_table_proof.json`. Frame has29 non-initializer pointer locations,
consistent with the48 instruction-use sites reconciled in V584.

This is not proof that any image is unused. An address can be calculated, passed
from elsewhere, loaded through a different resource object or replaced by an
embedded copy. The35 entries remain explicitly open where actual context is needed.

## Fifteen old Online paths differ from existing files

The initializer contains15 names such as `_pxl/Online06.pxl` that are absent from
the ROM filesystem. Same-basename files exist under `_pxl/online/`. The proof
records both facts, without assuming a runtime alias or changing the filenames.
These15 owners also lack external stored base-owner pointers. This does not
invalidate the separate already verified Online page loader or the user's
low-resolution Online artwork exception. It prevents treating a constructed old
object as proof of an available file/display path.

## Bounded calculated-address scan

An additional conservative scan follows AL constant arithmetic/register copies
and immediate base-memory operands within straight-line ARM blocks in every
main section and the declared overlay. Every transfer clears all constants;
runtime reads, indexed loads, Thumb and cross-branch/call flow remain unknown.
Decoded data may produce candidates, so instruction decoding alone is not
treated as reachability.

Seven candidates resolve:

- Six are the original frame/Confirm initializer field stores.
- `02085460 mov r1,fp` copies Frame's owner for the existing02085470 view setter.
  V584 already binds its source XYWH to `[80,216,8,8]`, outside the five small
  caption cells. It is not a newly found caption consumer.

There is no additional candidate in this bounded model. This is a useful search
boundary, not a global negative. Further work should prioritize genuine dynamic
selection, relative/indexed tables or embedded-copy readers instead of repeating
direct literal or this straight-line scan.

A separate marker diagnostic reused V584's argument propagator with owner02313F74.
Its inherited frame-caption intersection names do not describe marker content
and earn no caption credit. The dynamic112/X row helper02048098 has observed
direct selectors2,1 and an earlier-defined0, so those calls do not establish
Sell/Buy display. Marker price/header parent contexts remain open. The diagnostic
is retained under a clearly labeled subdirectory and is not an authoritative
native display proof.

## Reproduction and limits

- `scripts/trace_resource_owner_tables_v585.py` produces the source-bound
  catalogue and original cache-list contract in
  `work/analysis/resource_owners_v585/owner_table_proof.json`.
- `scripts/scan_owner_address_derivations_v585.py` produces the separately
  limited candidate list and its V584 crop binding in the same directory.
- `scripts/record_resource_owners_v585.py` binds those proofs/scripts, retains
  all18/22 original audit objects and archives the evidence under
  `E:/Rota Nova translations/Screenshots/Test fixtures/V585 Resource owners`.

There are no new emulator screenshots, guide candidates, ordinary-menu results
or hardware tests in this batch. No new Japanese caption requiring translation
was discovered. Existing graphics translations remain intact. All18 original
plaque/hint entries remain incomplete and all22 historical requirement objects
remain deep-identical. Five miniature captions, Confirm/marker/standalone-logo
contexts and other legacy/movie/material requirements remain open. The graphics
goal stays active and incomplete.
