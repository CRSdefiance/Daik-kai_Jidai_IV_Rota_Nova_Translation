# Workflow

## Milestone order

1. Inspect, manifest, and extract the clean ROM.
2. Resave without edits and compare all internal files.
3. Scan for candidate text.
4. Export and reinsert an unchanged script.
5. Change one short, known menu string in fixed mode.
6. Boot and inspect that string in an emulator.
7. Generate and reapply an xdelta patch.
8. Only then investigate pointer-table expansion.

Never edit the clean ROM in place. Keep ROMs outside version control and use a clean copy for
each experiment.

## Candidate scan

`scan` checks every internal file for CP932, UTF-16LE, ASCII, entropy, and an LZ10 header.
LZ10 content is decompressed for discovery. Compressed hits are intentionally excluded from
script export until recompression has been verified for the actual game resource.

Use repeatable `--include` path patterns to focus a scan after candidate containers are known.
Conservative mode drops low-confidence hits, resolves overlapping CP932/UTF-16 candidates, and
caps retained hits per file so binary-heavy resources cannot create unbounded reports.

The executable regions are exposed for targeted work as `/__arm9__.bin` and `/__arm7__.bin`.
They are scanned only when explicitly selected with `--include`.

## Confirmed ARM9 profiles

Use `extract-arm9-profile` for verified, repeatable extraction of the currently mapped
tables. `startup` covers title-menu and shared controller text, `characters` covers all
four playable-character records, `city` covers the mapped city-status labels and initial
Lisbon commodities, `menus` covers the first large shared-menu batch, and `all` combines
them. `world` covers recurring port-name slots. `--with-drafts` populates the known
fitting English translations.

Each profile verifies the clean ARM9 bytes at every offset before exporting. A mismatch
usually means the selected ROM is a different revision and is rejected. Profile entries
may map a verified zero-padded fixed slot when its English text needs more bytes than the
Japanese glyphs but still fits safely before the next table entry.

## Fixed insertion

Fixed mode verifies each row's `source_hex` against the chosen ROM. A replacement must encode
to no more than `source_length`; remaining bytes are padded with zero. Overlapping rows and
mismatched source bytes fail rather than risking silent corruption.

## Patch verification

`make-xdelta` creates a release manifest with clean-ROM, modified-ROM, and patch SHA-256
values. `apply-xdelta` enforces the manifest's exact clean-ROM hash before decoding and
the expected modified-ROM hash afterward. This is stricter than relying on the xdelta
stream alone.

## MESFILE / ILNK status

`/COMMON/MESFILE.DK4` is confirmed as an `ILNK` container with 41 blocks and an
end-sentinel offset. The tool can export 2,807 Japanese null-delimited records with
line feeds represented as `{LB}`, and a no-edit rebuild is byte-exact.

Some records contain multiple adjacent user-facing messages, so references may target
offsets inside a block or record. For safety, real MESFILE insertion currently requires
exact encoded byte length. Expansion must be enabled explicitly and remains experimental
until inner references are mapped.

Use `{HEX:NN}` to retain a leading speaker/control byte and a final `{PAD}` to fill a
shorter English translation with spaces to the record's exact original byte length.
Story text must also preserve the original position of every line-feed control:
`{LB@31}` pads toward byte offset 31, emits the line feed, and reserves a sacrificial
space because the renderer otherwise leaves the next ASCII glyph on the preceding
line. This keeps the intended first letter on the new line while leaving the
translation readable in CSV. Plain `{LB}` now reserves the same sacrificial space
without alignment. The rebuilder also preserves any leading ASCII spaces from the
Japanese record because these are consumed as layout bytes before the first English
glyph. Translators no longer need to add either protection manually.

The same renderer treats uppercase `F` and `I` as macro syntax. Only the verified
`FI`, `FA`, and `FO` name substitutions are allowed; validation rejects literal
capitalized English that would trigger those commands.

The four `/data/SC0.DK4` through `SC3.DK4` story files use the same ILNK container.
Strictly decodable Japanese records are exported; undecodable mixed-binary segments are
counted in metadata and retained byte-for-byte without replacement characters.

For larger revisions, `insert-script --batch` accepts compact
`dk4-ilnk-translation-batch-v1` JSON files. Each batch is locked to the clean internal
file's SHA-256, resolves stable record IDs against that verified file, and materializes
the full source-byte checks before rebuilding. Multiple batches can be combined with a
CSV in one insertion pass.
