# Actual gender-icon source crops and marker loading

V240 is research verification. V218 remains unchanged and the full graphics goal
is active. The preceding turn made progress on actual window resource loading.
This turn verifies two original marker consumers' gender branch/crop setup.

## Original crop branches

Both consumers reference the actual initialized `/_pxl/__marker.pxl` owner at
`02313F74`. Their original code chooses these cells:

| Symbol | Original source origin | Original crop | Full English symbol ink |
|---|---|---|---|
| Male, ♂ | (232,96) | 16×16 | All 7×7 symbol ink fits inside the original cell. |
| Female, ♀ | (240,112) | 16×16 | All 5×7 symbol ink fits inside the original cell. |

Execute the original branch fragments `02015870..020158DC` and
`02080470..020804E4` with both prior selector values. The source coordinates,
extent, owner and crop flags come from the original parent instructions; no crop
table or constructor arguments are replaced with the authoring boxes. The native
constructor returns all four expected views. Stack and both view guards pass.
All 66 symbol ink comparisons across the four crops pass, including the complete
arrow/cross and circles. Four native-cell source previews were visually reviewed;
the symbols and their original surrounding cell borders remain complete.

The first parent writes its view at object+`A0`; the second uses its original
object+`639C` literal. Both fragments end before their next unrelated parent call.
Prior selector values, scratch object bases and stack context are supplied. The
preceding character getters and surrounding parent logic are not executed, so this
does not prove the selector value for every character or physical screen placement.

## Actual marker resource load

The original initializer constructs the real marker owner. Native registration,
cache allocation, whole-image view construction, virtual copying and resource
resolution execute successfully. The complete header, palette and packed pixels
match V218, with native routine ABI and view guards intact. Only SDK filesystem
operations are bridged to the exact ROM; no owner, header or cache result is forged.
The marker remains 256×256. This also preserves all earlier captions in the atlas.

The four unreadable Online source images were inspected again, but no reliable
new body/chat transcription was recovered. No guessed text was added. Their source
dependency stays open while independent native graphics work continues.

## Evidence and remaining limits

- `scripts/verify_gender_consumers_v240.py`: execution and Ruff pass.
- `work/analysis/gender_consumers_v240/native_proof.json`.
- `work/analysis/gender_consumers_v240/four_actual_crop_previews.png`.

V173's controlled supplied-cell tests and V227's complete stored glyph checks
remain valid within their earlier scopes. V240 adds actual original crop setup;
it does not substitute those CPU checks for live GPU palette/alpha, complete
parent execution, input or gameplay. The embedded CMMNIMG copy's own consumer
is still unresolved. No ROM, patch, release profile or translation asset changed.

Four Online transcripts, remaining embedded/environmental/other display cases,
name consistency and final full-scope gameplay/integration remain unfinished.
Revisit older record-based checks at eventual goal completion as requested.

## Later live display evidence

[V242](person_info_display_v242.md) verifies both symbols in actual Sailor Info,
including complete cells/borders and the stored palette bank48 selected by field
0x30. Other parents and the embedded copy remain separately unverified.
