# Switch v89

v89 protects the capital I in the Intellect stat name and keeps each stat
increase and its amount together on one line. The fleet-power notice uses the
same one-line layout. v88's letter spacing and price-report fixes are included.

The build was checked by executing the game's native stat notification loop
with Intellect and Luck gains in an ARM64 test harness. Both gains fit on two
complete lines. The comparison also checked all six stat-name choices in all
four game languages and the other shared message entries.

The [manifest](manifest.json) records the hashes of the binary deltas, required
stock RomFS files, and all 18 final overlay files.

## Package a later verified overlay

Use the build inventory from the Switch authoring tools and give the packager a
new release directory. It creates the binary deltas and rebuilds the result
against the same stock RomFS before accepting the release.

```powershell
python -m switch.prepare_release --romfs "D:/my-dump/romfs" --overlay "D:/verified-overlay" --inventory "D:/verified-overlay/power-up-kit-campaign-report.json" --release "switch/releases/v90" --version v90
```
