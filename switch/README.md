# Nintendo Switch English localization

The Switch project targets the Japanese release of **Uncharted Waters IV with
Power-Up Kit HD Version**, update **1.0.2**, title ID `0100F0E0136BE000`.
[The v96 manifest](releases/v96/manifest.json) describes the current English patch.
The overlay includes all seven campaigns, shared UI and trade text, and English
graphics captions.

## Build v96

From the repository root, use Python 3.11 or later and install the project with
`python -m pip install -e .`. The Switch build reuses the repository's xdelta3
or pyxdelta support. Supply the `romfs` directory from your own extracted
Japanese 1.0.2 game. The output must be a new directory.

```powershell
python -m switch.overlay --romfs "D:/my-dump/romfs" --output "switch/generated/v96"
```

Use the resulting `exefs` and `romfs` folders together as one mod. Keep older
versions of the overlay out of the mod directory when testing. The builder
checks every required stock file and every patch by SHA-256, then verifies the
complete overlay before publishing it to the output directory.

Eden nightly `4089cfcffd` rendered Woodin's coastline and Basra city model
correctly in the Japanese game and the English localization during earlier
testing. Eden stable 0.2.1 stretched coastline textures in both builds.

## Keyboard and title logo

The name editor opens in English and switches between English and Japanese
in the same frame. v96 restores the HD title logo. See the
[v96 release notes](releases/v96/README.md) for the download and controls.

## Translation and maintenance

[The English catalogs](translations/README.md) identify scenario dialogue,
choice labels, voice variants, shared messages, and native UI wording by record.
The release deltas encode the tested native layout, commands, and graphics.
Use the inspector and layout checker to review extracted archives.
See the [v91 release notes](releases/v91/README.md) for the Palace fix,
the [v90 release notes](releases/v90/README.md) for the campaign review,
and the [v89 release notes](releases/v89/README.md) for the packaging workflow.
The repository's [game-file policy](../LEGAL.md) applies to
Switch development inputs and releases.
