# Promoted combined English build: V1492

Promoted on 2026-10-22 at the user's explicit request. This is the latest compiled,
verified cumulative checkpoint. The editorial and graphics goals remain unfinished.
The immutable construction baseline is retained so frozen earlier builds and source
locks remain reproducible. This promotion does not rebase that binary or mark every
included layer's gameplay audit complete.

## Apply the patch

Use your own unmodified Japanese ROM with SHA-256
`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`:

```powershell
python -m dk4tool apply-xdelta path/to/clean.nds releases/all_routes_unified_v1492/translation.xdelta --out out/all_routes_combined_v1492_candidate.nds
```

Expected ROM SHA-256:
`96d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd`.
Patch SHA-256:
`417db2ada9bc4a5ebfd552e6e2f81a8d57ba75369b6c3488eca6284b086867d0`.
The clean-input patch reconstruction was verified and its saved result rehashed at
promotion. Full ROMs, source ROM material, saves and RAM dumps are not distributed.

## What is included

All cumulative routes, graphics and English text through registered profile
`all-routes-unified-v1492`: 471 batches and 114 accepted layers. The latest build
integrates 32 source/native-reviewed battle reactions, with 16 revised and 16
retained. Original event coverage for those reactions is still pending.

The integration checks preserve earlier routes, graphics, fonts, controls and the
123040-byte staged payload. Targeted automated emulator tests cover startup and an
original capture/rewards/return-to-sailing control. A subsequent original stronger
fleet encounter reaches defeat, flagship transfer and normal sailing. Its sole
40-byte prebattle location fixture is disclosed. These are targeted checks, not
complete route playthroughs or physical-device verification.

## Known issue and unfinished work

Retreat notices 2683-2689 can interpret custom ship names such as `ICARUS` as speech
codes. The unintegrated V1509b/V1511b/V1512 research repairs name protection and passes
208 native font planes, but visual refinement, copy/cache regression checks, a
registered build and original transfer replay remain pending. **That repair is not
in this patch.** Its scripts/manuscript and explicitly labelled evidence are saved
with this checkpoint.

Editorial counts remain 1323 complete (985 revised, 338 retained), 1467 source/prose
reviewed and 144 reviewed-incomplete COMMON entries, with broader shared/route/raw
work still open. All 18 plaque audits remain incomplete; texture/border acceptance
does not close their remaining gates. The four low-resolution Online bodies retain
their earlier exclusion. Older record-based checks remain queued after the full
editorial goal.

## Reproduction records

`build_manifest.json.gz` is the byte-exact original build manifest; decompressed
SHA-256 `fdf9f572febb67d4cd6dfbfae2fbec5dc318fcaea1d9792e84955795b2ecc2ba`.
`build_release_stack.json.gz` preserves the exact registry used for that build,
before adding the promotion pointer. Both use standard gzip. `checksums.json`
covers the packaged artifacts. `promotion.json` records the user's request, scope,
hashes and open issue. `verification/` includes integration, reconstruction and
original-event records; the research font proof is explicitly unintegrated.

The ROM remains at
`E:/Rota Nova translations/Generated/out/all_routes_combined_v1492_candidate.nds`.
Git tag: `promoted-v1492`.

See [integration checkpoint](../../docs/battle_reactions_v1499_integration_checkpoint.md)
and [promotion and research status](../../docs/promoted_v1492_checkpoint.md).
