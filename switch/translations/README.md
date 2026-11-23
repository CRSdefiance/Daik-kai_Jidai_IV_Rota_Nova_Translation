# Switch English catalogs

These are the English records from the verified v89 overlay. Scenario JSONL
files `sc0` through `sc6` correspond to Raphael, Hodram, Lil, Maria, Saiki,
Woodin, and Tial. Every line identifies a native scenario block and record,
with a turn for dialogue, a slot for a choice, or style slots for voice variants.
Offsets are relative to the block. The shared catalog uses `group:record` IDs.
The native wording catalog records platform-specific labels and format strings.

Keep substitution tokens and native formatting markers when reviewing a line.
Full-width F and I are protected in the stored script. The Switch renderer
draws them with standard Latin spacing. Use
`python -m switch.inspect_script --help` and
`python -m switch.check_layout --help` from the repository root.

The release builder applies the tested binary deltas, which also carry native
commands and graphics. Text changes need to be integrated into a new overlay
with the Switch authoring tools, then packaged as a new release.
