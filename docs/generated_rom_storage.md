# Generated ROM storage on E

For current cleanup rules and the preview/apply command, see
[generated ROM retention](rom_retention.md). The migration counts below describe
the original move, not the current archive inventory.

The user requested moving all generated ROMs to `E:\Rota Nova translations`.
The completed migration physically stores 1,042 ROMs under its `Generated` folder,
preserving the original `out` and `work` subfolder structure. This includes thirteen
test-generated clean copies that the initial filename-based estimate excluded.
The original input `work/clean.nds` remains on C with its exact original hash.

All 20,164 copied files, including ROMs, patches, manifests and associated research
records, passed SHA-256 comparison before their C copies were removed. Sixteen
directory junctions preserve existing build, verifier and documentation paths.
Individual file links required administrator rights; tested folder junctions did not.
No administrator credentials or approval were needed.

Three standalone root-work roundtrip ROMs had no references in repository code or
documents and were moved to `Generated\work`. Their old/new paths and exact hashes,
along with every migrated ROM and package/junction, are recorded in
`translations/generated_rom_storage_move.json`. The migration script is
`scripts/move_generated_roms_to_e.ps1`; do not rerun it over an existing receipt.

The latest verified release files remain convenient top-level copies in
`E:\Rota Nova translations`, with finalized guide images in `Screenshots`.
The generated archive contains historical, experimental, revoked and research
artifacts. File presence there is not a release-quality or acceptance claim.

Future playable builds written to `out` and research builds written under
`work/analysis` physically go to E through the preserved junctions. New test-ROM
temporary folders should use `E:\Rota Nova translations\Generated\work\tests`.
`translations/release_output_destination.json` records this policy. Source code,
translation documents and synced `sources` are not relocated.

Post-migration V388 verification succeeds through the original logical paths:
exact clean patch reconstruction, all470 inherited batches/stages, three actual
cold-boot string pointers and65 unchanged gameplay frames. This storage request is
complete; the broader graphics goal and all remaining plaque/display gates stay open.
