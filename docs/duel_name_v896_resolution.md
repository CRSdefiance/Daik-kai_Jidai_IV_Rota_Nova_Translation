# V896: duel first-name audit correction

The V894 lead confused the user-approved middle name Joakim with the first name. The existing documented decision is **Hodram Joakim Bergstrom**:retain the faithful first-name adaptation Hodram rather than original Latin Hoodlum,and use Joakim rather than Joachim for the middle name. See `translations/character_name_localization_policy_v1.json`.

Unmodified V893 cold-boots with no cartridge save,savestate,unlock or RAM/ROM fixture. The retained RIGHT input selects genuine captain1. His actual fresh17-byte name fields at actor+32/49/66 are Hodram/Bergstrom/Joakim. The original duel actor pointer resolves the same actual captain;its virtual name getter0201371C returns actor+32,Hodram. The getter and setup match clean code. All6144 actual source-name bitmap cells match independent original font cells,including first/final letters and blanks. The duel first-name label is correct.

No name patch,player-name overwrite,save or artwork edit is warranted by this lead. The older source donor may still contain historical middle-name spellings;this proof does not certify every save,caption or name consumer. The distinct Samwell header and separate graphics/all18 plaques remain open. Historical V894 observations are retained;this successor records the corrected interpretation. No prose or completion credit is added.
