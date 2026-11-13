# V509 complete registered PXL cache loading

Previous goal turn: progress, V508 shared Tavern formatting repair and publication.
V508 remains unchanged. This turn extends native loading evidence; no graphics,
ROM, patch, save or gameplay state changes.

## New evidence

The original full startup driver `02005310` reaches all 41 constructor entries.
It creates 372 named PXL owners, resolving 356 distinct ROM files. This registration
coverage was already established in V385; the initial two-function investigation
in this turn repeated partial coverage and is not counted as new completion.

The new verifier executes the original cache getter `020D6558` for **all 356
existing registered files**, then repeats each load while hot. All 712 returns
preserve the native stack and saved registers. Every complete header, palette and
pixel payload matches the actual current ROM bytes. Every returned data extent
is inside the original cache pool; no SDK handles remain open. Warm loads return
the same pointer and bytes with no further filesystem operation.

Only SDK filesystem open/read/seek/close is bridged to exact ROM data. Original
registration, cache allocation and resolution code executes. No owner,
filename, header or graphics payload is substituted. These supplied owner calls
are native cache-loading evidence, not actual scene selection or GPU evidence.

All four bytes of every registered filename pointer were observed during the
loading sequence; none changed. Both formerly ambiguous generic-reader callsites
`02047888` and `02047BA0` use literal owner `02313F38`, the original item-atlas
owner with filename `_pxl/item.pxl`. They are not arbitrary supplied-owner bindings.
This does not establish that the filename can never be changed by unrelated code.

The initial observer inspected 372 fields on every memory write and was too slow.
Its identified read-only process was stopped. The replacement uses byte membership
lookups and also catches partial pointer writes; the identical full test scope
then completed normally. No timeout alone was treated as test completion.

## Current loading coverage and remaining consumers

V385's 300 event/town staging cases remain bound to current V508 through exact
file hashes and unchanged original loader code. Together with the new 356 cache
cases, native file-loading evidence covers **656 of the 660 PXL files**.

The remaining original consumers are still unresolved:

- `/_pxl/copyright.pxl`: original Latin copyright/date retained.
- `/_pxl/logo.pxl`: existing English Uncharted Waters IV / Rota Nova retained.
- `/_pxl/ship_eurL.pxl`: original ship-material texture retained.
- `/_pxl/startmenu0.pxl`: existing English Porto Estado edition art retained.

Their source decisions were already reviewed in V386. Fifteen bare Online filename
owners have no corresponding exact path and are not selected by the 13 known active
Online page tables. They were not loaded, renamed or declared globally unused.
The user exemption for low-resolution Online screenshot translation remains.

Neither this coverage nor the absence of raw DK4 reads in these PXL calls proves
legacy archives unused. Raw comic, eleven legacy composition gates, FLS and actual
scene crops/alpha/gameplay remain separate requirements. All 22 historical items
and all 18 incomplete plaque entries remain in the audit. The goal remains active.

## Evidence

- `work/analysis/resource_registry_v509/registry_proof.json`.
- `work/analysis/resource_registry_v509/cache_load_proof.json`.
- `work/analysis/resource_registry_v509/coverage_proof.json`.
- `scripts/research_resource_registry_v509.py`.
- `scripts/verify_registered_cache_loads_v509.py`.
- `scripts/reconcile_pxl_loader_coverage_v509.py`.

Candidate: V508, SHA-256
`c7b86f93ad034bf5c19aa82a51cecb4194ace6dcdce23e481e67c24074bbfbcb`.
It remains experimental; no canonical promotion or new release artifact.
Revisit older record-based checks at actual full-goal completion.
