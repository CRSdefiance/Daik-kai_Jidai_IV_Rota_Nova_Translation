# Narrow English Options confirmations

## Source and scope

Integrated experimentally in V144 with the complete V143 renderer stack.
Saved-ROM preservation, canonical checks and exact patch reconstruction pass;
see `all_routes_unified_v144_checkpoint.md`. The research-only statements below
describe the earlier probe. Physical gameplay and acceptance remain pending.

Clean prompt `0213880C` states the current setting for at-sea operation help and
asks whether to change it to the second substitution. `02138844` does the same for
income/expense reporting. The existing menu labels are Sailing Help and Reports.
The research English uses those established labels in complete natural sentences:

- `Sailing Help is %s. Change to %s?`
- `Reports are %s. Change to %s?`

The current tense preserves the original current-setting meaning. Both argument
orders remain current state then proposed state. No manual line breaks or padding
spaces are authored. Source allocations remain 56 and 52 bytes respectively.

## Native evidence

Actual Options callers `0203FCD0` and `0203FD54` select the two On/Off arguments,
then execute varargs wrapper `020546F8`, CE898 and original macro expansion through
`0205479C`. Ten flag cases retain full narrow prose and untouched preferences.
Twenty actual post-confirmation response cases preserve cancellation and every
unrelated preference bit; affirmative choices toggle only the correct bit and
set the native dirty flag.

Eight native shared-modal raster cases match full glyph order and independent
pixels in both formats. The V142 raster code/font bytes and resident prefix are
verified unchanged in V143; renderer execution uses that exact original resident
section. All four resulting state panels are inspected in
`work/qa/options_narrow_native/native_sheet.png`. Complete sentences fit one row;
leading/final characters and state names remain intact.

Evidence: `work/analysis/options_narrow_prompts_proof.json` and disposable
`options_narrow_prompts_arm9.bin`. No playable ROM/profile changes. The historical
ASCII-corruption warning remains applicable to older builds: this research proves
the current scoped path, not arbitrary ASCII replacement. Full widget/choice/input,
physical routing and cold-boot gameplay remain pending before acceptance.
