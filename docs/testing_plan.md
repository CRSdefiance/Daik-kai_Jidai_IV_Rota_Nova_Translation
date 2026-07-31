# Testing plan

## Automated

Run `pytest`. All default tests use synthetic, copyright-free bytes. Real-ROM tests must be
marked `integration`, use `DK4_NDS_ROM`, and skip when it is absent.

## Manual emulator smoke test

For every candidate build:

1. Boot the clean ROM and modified ROM.
2. Confirm title screen and first controllable scene.
3. Inspect every modified screen for text, clipping, glyph errors, and crashes.
4. Exercise new game, load/save, port, tavern, shipyard, trade, sailing, battle, and options
   as they become part of the translated surface.
5. Save, quit, reload, and confirm the save and modified text remain functional.
6. Revisit all previously translated screens before release.

Record the area, expected and observed English, clipping, bad glyphs, crash status, screenshot
path, emulator/version, and pass/fail result.

## Patch verification

Create an xdelta patch, apply it to the same clean ROM, compare the rebuilt ROM hash with the
modified ROM hash, and boot the rebuilt copy. A wrong source should fail or yield a hash that
does not match the release manifest.

The tool enforces the source and target SHA-256 values from `release_manifest.json`.
Automated tests cover native xdelta encode/decode and rejection before decoding when the
source hash is wrong.
