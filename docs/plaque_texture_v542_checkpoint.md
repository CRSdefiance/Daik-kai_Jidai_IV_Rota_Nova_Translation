# V542 plaque texture checkpoint

The previous goal turn made progress: it produced source-grain prototypes for
17 plaques and exposed the inherited donor mismatch. This turn resolves two
overlapping crew rows, registers the complete V542 integration, and verifies the
actual production candidate on both screens. The result remains experimental.

See [build notes](../work/analysis/plaque_texture_v542/BUILD_NOTES_V542.md)
and [open texture defect](plaque_background_texture_defect.md).

The 17 complete font masks and all 61 native plaque crops pass. All 56 fresh
regression frames are exact V540, all 921 graphics metadata/palette/extent checks
pass, and the clean patch reconstructs the candidate exactly. Only the two
plaque atlases change from V540; all game code and other translations are retained.

Source grain is reconstructed from two original blank strips, not recovered
exactly under the original lettering. Existing bevel pixels are retained rather
than proven against each Japanese original. Town plaques and dynamic hints are
not corrected by this release. Keep all 18 inventory entries incomplete, retain
all 22 requirements, and continue the full graphics audit.
