# Lil SC2 B206 ceramic-earrings control note

B206 contains 29 source records: 28 dialogue or choices and one packed event.
R0015 is `35 48 8A A8`, identical to Hodram SC1 B210's verified nontext item
payload; it is excluded unchanged.

`AD`, `02`, and `07` are the merchant, Lil, and Cristina presentation states.
R0059/R0061 begin with Shift-JIS `82`, R0080 with `94`, and R0082 with `8D`.
These four records are bare choices. The B206 profile removes these bytes
from speaker detection, so Got it/So?/Buy/Pass retain G/S/B/P as their first
encoded glyphs. B204 retains its separate profile for the genuine `82` lord
state.

The source meaning, 9,000-coin price, dancer legend, information motive, and
all refusal branches were reviewed. English fits the original byte slots,
avoids unsafe literal uppercase I/F, and uses the formatter for wrapping.
All 28 text records pass QA with zero error or warning blockers. Three contact
sheets were visually checked. Saved-ROM verification confirms every edit and
the unchanged item payload. Event behavior still requires runtime review.
