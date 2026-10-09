# Alternate title display verified through Extras

V238 is a verification iteration. The registered ROM remains V218, SHA-256
`be05e432cda1b32c18f6b1fbca8c57d6069a442ea87c2c158388fe38f3d5220f`.
The preceding naming-documentation turn confirmed existing decisions and made no
new goal progress. This turn supplies new physical framebuffer evidence.

## Observed display and navigation

The previously unobserved `/_pxl/title/title05.pxl` appears on the upper screen in
**Extras**, including its **About Extras** explanation. Normal START, DOWN and A
input reaches these screens. B returns to Extras; another B returns to the main
menu. The three navigation captures at frames 2100, 2500 and 3000 were visually
reviewed. The explanation is readable and both menu returns are visible.

Two independent cold boots provide fifteen complete upper-screen matches:

- Six Extras captures in the first boot match title05 exactly.
- Six Extras/About Extras captures in the navigation boot match title05 exactly.
- Three captures after returning to the main menu match title03 exactly.

Every match checks all 49,152 pixels at native 256×192 resolution, totaling 737,280
pixel comparisons. Both complete logos, first and last letters, gold flourishes,
shadows, edges, background and screen bounds are included. Palette channels are
compared at their native five-bit precision. There is no missing letter, crop or
opaque padding defect in these observed displays.

The pinned DeSmuME core uses interpreter mode, one core, English firmware and
native software rendering. No savestate or RAM injection is used. All recorded
PNG identities, ROM identity, input schedules and empty callback-error lists pass.
The final RAM files are read-only exports. Both emulator processes are terminal.

## Evidence and limits

- `scripts/verify_alternate_title_v238.py`: verification and Ruff pass.
- `work/analysis/alternate_title_v238/native_display_proof.json`.
- `work/emulation_v193/alternate_title_v238/capture_report.json`.
- `work/emulation_v193/alternate_title_v238/navigation/capture_report.json`.

V229 already verified native title05 registration, loading and view copying. This
result closes its previously open physical display question for the observed
Extras states. It does not identify the standalone `/_pxl/logo.pxl` consumer,
prove every fade or device, or imply user cold-boot acceptance. Four unreadable
Online bodies, other embedded/environmental consumers, naming consistency and
remaining gameplay/integration requirements keep the full goal active.

No ROM, patch, release profile or translation asset changed. The user-requested
review of older record-based checks remains due at eventual goal completion.
