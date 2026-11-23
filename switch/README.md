# Nintendo Switch English localization

The Switch project targets the Japanese release of **Uncharted Waters IV with
Power-Up Kit HD Version**, update **1.0.2**, title ID `0100F0E0136BE000`.
[The v89 manifest](releases/v89/manifest.json) describes the current English patch.
The overlay includes all seven campaigns, shared UI and trade text, and English
graphics captions.

## Build v89

From the repository root, use Python 3.11 or later and install the project with
`python -m pip install -e .`. The Switch build reuses the repository's xdelta3
or pyxdelta support. Supply the `romfs` directory from your own extracted
Japanese 1.0.2 game. The output must be a new directory.

```powershell
python -m switch.overlay --romfs "D:/my-dump/romfs" --output "switch/generated/v89"
```

Use the resulting `exefs` and `romfs` folders together as one mod. Keep older
versions of the overlay out of the mod directory when testing. The builder
checks every required stock file and every patch by SHA-256, then verifies the
complete overlay before publishing it to the output directory.

## Translation and maintenance

[The English catalogs](translations/README.md) identify scenario dialogue,
choice labels, voice variants, shared messages, and native UI wording by record.
The release deltas encode the tested native layout, commands, and graphics.
Use the inspector and layout checker to review extracted archives.
See [release preparation](releases/v89/README.md) for the packaging command and
v89 checks. The repository's [game-file policy](../LEGAL.md) applies to
Switch development inputs and releases.
