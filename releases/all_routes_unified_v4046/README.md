# Main promoted English build: V4046

Promoted on 2026-10-26 at the user's request. This is the current main cumulative
build, containing 539 manuscript batches and 114 accepted layers. Earlier releases,
ROMs and translations are preserved. The full editorial and graphics goals remain
active. Tag: `promoted-v4046`.

## Apply the patch

Supply your own unmodified Japanese ROM with SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v4046/translation.xdelta --out out/all_routes_combined_v4046_candidate.nds
```

Expected ROM SHA-256:
`6b991313e0f31e72b2548b7fd024ca406b710f61d56ddc35c06e147a443e4913`.
Patch SHA-256:
`56f13528927f23cd5c72f45fde79fbed58ab6d463d0ad2c916e149fc4b66c971`.
The complete reconstruction was rerun and compared byte for byte at promotion.
ROMs, saves and raw RAM captures remain local.

## Included work and verification

The registered cumulative profile is `all-routes-unified-v4046`. It preserves the
earlier shared text, UI, graphics, fonts and four routes. Its latest integrated
editorial batch is Lil SC2 B165: 24 contextual reviews, 14 revisions and 10 justified
retentions. Against V4002, only that SC2 block changes; every other file/component
and the 123040-byte staged payload remain exact.

Existing targeted automated emulator tests include two registered opening/town
cold boots, 31 complete framebuffer comparisons and five actor/captain controls.
The B165 content-fixture tests display 23 distinct speeches and normal town return;
one conditional speech has offline native coverage only. Source commands and
conditions are preserved as documented, with the recruitment effect omitted from
the disclosed content fixture. These tests establish scoped display and transition
coverage. They do not establish natural event eligibility, earned recruitment,
complete route playthroughs or physical-device verification. Promotion adds no new
gameplay or user cold-boot claim.

## Unfinished work

The authoritative ledger records 5529 completed contextual reviews, including 3527
historically revised and 2002 retained, and 5532 source/prose reviews. B166 has 44
additional native-approved objects (24 revisions, 20 retentions), stored separately
without new source/prose or completion credit. **Those revisions are not in this
ROM.** Relocation, final stored references, representative story/choice returns,
integration and release checks remain pending. Its three focused menu-only cold
boots establish complete labels, highlights and actual backing ownership; they
do not display the B166 speeches or accept a menu outcome.

All wider storylines, shared shop/town dialogue, random scenes and remaining prose
remain within the active editorial goal. Preserve COMMON 750-752, canonical Maria
SC3 B97, remaining B167-B180 and other recorded prose leads. Graphics and all 18
plaque audits remain separate; the later older-record technical re-audit stays
queued. See the [current handoff](../../docs/editorial_handoff_current.md).

## Reproduction records

`build_manifest.json.gz` and `build_release_stack.json.gz` preserve the byte-exact
original build manifest and build-time registry. Their decompressed hashes are
recorded in `promotion.json`. The current registry changes only the promoted-build
pointer; the frozen build inputs remain intact. `checksums.json` covers every other
packaged file. `verification/` contains the original scoped verification receipts,
promotion reconstruction record and explicitly labelled unintegrated B166 proofs.
Historical receipts describe their original checkpoint; the final package audit
records current promotion and ledger status.

At promotion, 91 selected dialogue and integrated-release tests passed. Three
historical integrity tests stopped before auditing because their V5 ROM fixture
is absent; see `verification/promotion_test_results.json`. The current V4046
registered verification and independent promotion audit passed.

The immutable construction baseline remains
`out/raphael_natural_v2_accepted_base.nds`, SHA-256
`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
This promotion follows the V1492 checkpoint workflow without rebasing frozen
construction inputs or changing accepted-layer status. The registry schema still
labels buildable profiles `experimental`; the separate promotion record designates
this main build. The local ROM is retained at
`E:/Rota Nova translations/Generated/out/all_routes_combined_v4046_candidate.nds`.
