# Switch 1.0.2 English localization v94

Press X or select OK while the English keyboard is open to use the game's
usual name confirmation. L and R move the caret one character at a time.
B deletes one character when the field contains text and cancels when the
field is empty. The corresponding controller icons remain visible on the
editor. Use `あ` or `Aa` to switch layouts.

In Eden Nightly `4089cfcffd` with Vulkan, pressing X from the English
layout opened the ship-name confirmation, and the accepted name appeared
in Refit. The character editor accepted an edited first name, a blank
middle name, and the last name from the English panel. The runtime test
also exercised the layout switch in both directions and checked that the
caret and backspace move one character at a time in mixed-width text.

For an existing v93 installation, replace the
[ExeFS IPS](patches/exefs/B0AF08523E1F31067BB9E170532047AC96A1C9EF.ips).
The [manifest](manifest.json) covers the 18 loose overlay files. To rebuild
the full overlay from a Japanese Switch 1.0.2 RomFS dump, run this from the
repository root.

```powershell
python -m switch.overlay --manifest switch/releases/v94/manifest.json --romfs "D:/my-dump/romfs" --output "switch/generated/v94"
```

To regenerate the ExeFS patch, run `python -m switch.build_name_keyboard`
with Keystone, the uncompressed Japanese 1.0.2 main NSO, and the v91 IPS.
