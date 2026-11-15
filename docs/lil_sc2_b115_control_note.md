# Lil SC2 B115 control mapping

B115 starts with Lil (`02`) and Janus Pasha (`04`) examining a stone tablet.
Companion variants begin with ordinary Japanese text (`82/92`), except the
selected companion's `D0` state. Their English begins with the first visible
letter rather than an invented presentation command.

From R0061, this is a shared Maria branch. Source-identical records in SC0 B123,
SC1 B123, and SC3 B97 corroborate Maria (`03`), the African raider (`B4`), and
the whisper/scene sound (`FE`). Maria challenges the raiders' indiscriminate
revenge and recruits them to oppose the great powers. Preserve these identities
within SC2; do not relabel Maria as Lil.

R0078 retains the runtime faction macro `{MACRO:FO}` and the route profile's
nine-cell expansion. Its short allocation requires the concise "With FO."
R0089 starts with `0A`, which is a staging newline, not a speaker byte. The
English starts with `B` in "Bold words" on the first row. The profile must not
classify `0A` as a speaker selector.

All 37 records pass fixed-allocation QA and visual preview review. The tablet
scene, shared Maria branch, portraits/nameplates, faction expansion, R0089's
opening letter, continuation letters, recruitment reward and transitions need
a cold-boot sample before acceptance.
