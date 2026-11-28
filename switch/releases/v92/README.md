# Switch 1.0.2 English localization v92

The name editor opens on the Latin alphabet. The `あ` key opens the
Japanese panel, and `Aa` returns to Latin. The Latin keyboard keeps
fixed-width key cells, including `I` and `F`. Custom names display with
proportional Latin letters. The game keeps its original name encoding, so
existing saves can use the new spacing without renaming anything.

[The manifest](manifest.json) contains the replacement ExeFS patch and
the matching RomFS files. To rebuild the loose overlay with a Japanese
Switch 1.0.2 dump, run this from the repository root.

```powershell
python -m switch.overlay --manifest switch/releases/v92/manifest.json --romfs "D:/my-dump/romfs" --output "switch/generated/v92"
```

The v92 ExeFS patch is included in this release. The keyboard builder now produces v93.
