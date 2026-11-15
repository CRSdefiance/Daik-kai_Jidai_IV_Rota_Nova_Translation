# Lil SC2 B109-B110 control mapping

B109 is the Colosseum doubling-bean riddle, including both wrong answers and the
correct 59-second branch. B110 is the urn tablet's left-hand puzzle and its
immediate outcome. The V29 batch was reviewed against the clean Japanese SC2
text and the connected scene before encoding.

The leading bytes `02` (Lil), `09` (Kamil), `97` (sailor), `CF` (party), `D0`
(selected crewmate), and `FE` (Colosseum voice or inscription) are presentation
states. Each translated record keeps its exact state through `{SPEAKER:XX}`.
The Japanese first bytes `81`, `82`, `83`, `89`, `8D`, and `92` are ordinary
Shift-JIS text starts in these blocks, including answer choices and companion
variants. Their English starts immediately with its first visible character;
none receives a speaker selector. The two Kamil records B109 R0076 and R0165
retain the three-byte `FI` runtime name macro through `{MACRO:FI}`.

B109 R0281 is the six-byte fragment `96 47 21 48 51 A8`. It does not decode as
coherent prose in scene context. V29 explicitly excludes it and leaves its
bytes unchanged pending a runtime control mapping. The source-leading blank
rows in B109 R0013 and R0024 are staging; their English begins on the first
visible row.

All 73 dialogue records passed the fixed-box audit and preview review without
manual line breaks or missing first glyphs. Runtime presentation still requires
a cold boot through the riddle's three branches and the urn's choices.
