# Switch 1.0.2 English localization v96

v96 restores the HD title logo that was on Google Drive before the
v95 release. The v95 publication used an older title archive from
the DS-logo build.

The v95 keyboard controls apply to v96. The editor opens in English,
and `あ` and `Aa` switch layouts in the same frame. Press X to confirm
directly from English. The title archive is the only changed file.

The [manifest](manifest.json) covers the 18 loose overlay files. For an
existing v95 installation, replace `romfs/TitleJP.dk4` with the one from
the [Drive patch folder](https://drive.google.com/drive/folders/1FkCnc5MJGHulhcfU_LVWchQE_EvjAHsQ).
To rebuild the full overlay from your Japanese Switch 1.0.2 RomFS dump,
run this from the repository root.

```powershell
python -m switch.overlay --manifest switch/releases/v96/manifest.json --romfs "D:/my-dump/romfs" --output "switch/generated/v96"
```
