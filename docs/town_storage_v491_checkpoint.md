# V490-V491 storage controls; no production change

V484 remains current, SHA-256
`f2036bafc3736a353cb0a2de8f40bd5eee8bed3cd16e779f68e3ebb1914b875c`.
V488 stays revoked. All22 historical requirements and18 incomplete plaques remain.

## Ownership-guard control V490

Cleanup checks whether the saved bitmap pointer's block is present in the current
SDK heap's used list before calling the original free API. It still produces the
same failed help interval15200-21200 and undefined instruction. Merely checking
used-list membership is therefore not a valid repair. Exact retained references,
allocation identity and object invalidation mechanism remain unproven.

Assembly/manifest: `work/analysis/town_canvas_owner_v490`.
Terminal report: `work/emulation_v193/town_canvas_owner_fresh_v490/capture_report.json`.

## Zero-additional-allocation control V491

The town view uses a private20-byte header in fixed SDK padding and renders into
the existing temporary graphics buffer at02233040. No malloc/free is added; the
original shared numeric header and VRAM backing are not redirected. The helper
clears15104 bytes and copies8208 original numeric pixels on each town draw.
This is a research sharing contract, not proof that the buffer is exclusively
available to the town panel.

- M28 substitution frame3700 displays the Hodram name card.
- Fresh21200-frame run does not crash.55 of56 reference capture hashes match;
  frame15200 differs and is not silently cleared as equivalent.
- Genuine Istanbul captures differ from3600 onward. Visual review shows colored
  corruption in the upper town information panel. Existing shared temporary
  storage is therefore unsafe in this implementation and is not a release fix.

The positive movie result does not compensate for damaged town artwork. Both
controls leave production graphics/scripts/progression untouched; neither is
distributed or promoted. No current full-movie, ending-unlock or full-goal credit.

Sources/manifests: `work/analysis/town_scratch_v491`.
Reports: `town_scratch_fresh_v491`, `town_scratch_movie_v491` and
`town_scratch_town_v491` under `work/emulation_v193`.

## Next work

Provide properly owned rendering storage without the persistent allocation that
interferes with movie loading or the temporary-buffer aliasing that damages the
town panel. Preserve all124 English commodity names, numerical UI and existing
graphics. Full help, actual town and movie rendering gates remain required.
At actual goal completion, revisit older record-based checks.
