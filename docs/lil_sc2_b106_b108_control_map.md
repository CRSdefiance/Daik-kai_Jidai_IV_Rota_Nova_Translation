# Lil SC2 B106 and B108 presentation states

These source-byte identifications support an experimental Lil layer.

| Lead | Source and context evidence | Role in these blocks |
|---|---|---|
| `02`, `09` | Established Lil and Kamil selectors | Lil; Kamil |
| `10`, `14` | Earlier Lil batches and profile | Gerhard; Fernando |
| `D0` | Established selected-crew selector from B103-B104 | Selected crewmate |
| `B1`, `B2` | B106 R0010/R0014 and subsequent cult lines match SC0/SC1 B115 source bytes | Megalith cult leader; cultists |
| `A0` | B108 R0006/R0009/R0012 match SC0/SC1 B117 source bytes, where it marks the hidden believer; B106 uses the same selector for the village speaker who confronts the cult | Village speaker; hidden believer, by scene |

The B106 variants beginning `82` and `89` and B108's other ordinary text retain
their first Shift-JIS glyph during source reading. B106 R0232 and R0236 begin
`89 BD` (何), so `89` must not become a speaker selector. The translated line
must start with its first English character. The renderer's guarded, pair-phase
formatting protects continuation starts.

Static byte evidence does not confirm portraits, names, or branch flow. Those
effects require a cold-boot check of the integrated candidate.
