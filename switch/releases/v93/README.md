# Switch 1.0.2 English localization v93

The name editor opens with the Latin panel selected. Press X to use the
editor's OK action from that panel. The `あ` and `Aa` keys switch between
Japanese and Latin.

The preview and caret use the same font measurements. The Latin grid
keeps its fixed-width key cells, while names in the editor and across the
game display with proportional Latin letters. Names use the game's
original save encoding.

Eden Nightly `4089cfcffd` with Vulkan opened the Latin panel in the ship
editor. Controller input entered Valor, and the caret appeared after the
final letter. Pressing X opened the usual ship name confirmation. Valor
displayed with proportional spacing next to Carteira in the refit list.

The [manifest](manifest.json) covers all 18 loose overlay files. If v92
is installed, replace the [ExeFS IPS](patches/exefs/B0AF08523E1F31067BB9E170532047AC96A1C9EF.ips)
to test v93. To rebuild the full overlay, use a Japanese Switch 1.0.2
RomFS dump from your game and run this from the repository root.

```powershell
python -m switch.overlay --manifest switch/releases/v93/manifest.json --romfs "D:/my-dump/romfs" --output "switch/generated/v93"
```

The ExeFS patch can be regenerated with `python -m switch.build_name_keyboard`,
Keystone, the uncompressed Japanese 1.0.2 main NSO, and the v91 IPS.
