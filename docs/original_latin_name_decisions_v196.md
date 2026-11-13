# Original Latin character-name decisions

**Historical proposal, partly superseded on 2026-10-06:** the user chose to keep
Hodram and to prefer faithful, sensible localization where it improves on original
Latin lettering. The source-card evidence below remains valid. Its Hoodlum
migration and absolute Latin-spelling priority are not current instructions.
Follow `docs/glossary.md` and `translations/character_name_localization_policy_v1.json`.

The user resolved the naming question in favor of names established in original
Latin artwork. Full source cards confirm **Rafael Castor**, **Hoodlum Joakim
Bergstrom**, and **Camille Overijssel**. **Lil Argot** already agrees.

The preferred spellings are now recorded in `docs/glossary.md`. Preserve this
original artwork and bring translated text into agreement with it.

## Evidence and remaining implementation

`scripts/audit_original_latin_names_v196.py` checks clean, canonical and V190 M28
textures 22, 46 and 71. Their dimensions, palettes and entire index buffers agree.
Individual source renders and their hashes are saved under
`work/qa/original_latin_names_v196/`; the report is
`work/analysis/original_latin_names_v196.json`.

The report inventories **187 effective active-batch records** carrying older
spellings. It resolves superseded manuscript records by registration order. This
is a source inventory: terminal shared names, biography data, runtime macros and
baked canonical records also need inspection before claiming complete migration.

Implementation must preserve clean-source locks, executable speaker commands,
formatting guards and all existing release layers. Reformat logical English rather
than replacing encoded bytes. Review allocations and macro expansion lengths:
Raphael (7) to Rafael (6) and Hodram (6) to Hoodlum (7) change ASCII pair parity;
Kamil (5) to Camille (7) increases capacity needs without changing parity.

No ROM, patch, source batch or accepted release was changed by this decision audit.
V190 remains the latest experimental candidate. The graphics goal remains active;
name migration and its native rendering checks remain required work.
