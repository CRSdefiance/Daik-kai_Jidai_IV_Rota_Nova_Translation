# Switch 1.0.2 English localization v95 test build

The name editor opens with one English keyboard. Select `あ` to switch to
Japanese and `Aa` to return to English. The layouts share the same frame
and preserve the text and caret. Press X or select OK from the English
layout to confirm the name.

In Eden Nightly `4089cfcffd` with Vulkan, both the character and ship
editors opened in English, switched layouts in place, preserved entered
text, and accepted X from English. The longer Japanese character list
and its scrollbar fit within the shared frame.

For an existing v94 installation, replace the
[ExeFS IPS](patches/exefs/B0AF08523E1F31067BB9E170532047AC96A1C9EF.ips).
The [manifest](manifest.json) covers all 18 loose overlay files. To rebuild
the full overlay from a Japanese Switch 1.0.2 RomFS dump, run this from the
repository root.

```powershell
python -m switch.overlay --manifest switch/releases/v95/manifest.json --romfs "D:/my-dump/romfs" --output "switch/generated/v95"
```

To regenerate the ExeFS IPS, run `python -m switch.build_single_name_grid`
with Keystone, the uncompressed Japanese 1.0.2 main NSO, and the v94 IPS.
