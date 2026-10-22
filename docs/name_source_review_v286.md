# Source/context review for integrated naming V286

Previous turn made progress on real native Gallery description selection,
composition and original-overlay clearing. This turn reviews the first100 current
name-migration records against clean Japanese and spoken context:99 reviewed,
one held. This is a prerequisite to combining locked names with artwork captions.

## Three fuller source-faithful corrections

| Record | Complete revised translation |
|---|---|
| SC0B218R0109 | We don't want anything to do with you either! Let's go, Rafael! |
| SC0B223R0040 | Oh, Admiral Rafael! Listen, there was a pair of swans here. |
| SC0B227R0020 | Yes, I'm Rafael Castor. What can I do for you? |

The first preserves Claudio's retort to the merchant's own dismissal; the second
preserves Christina's title and conversational lead-in; the third makes Rafael's
full-name introduction a complete spoken sentence. Actual macros and actor bytes
remain. The clean source and canonical source are locked independently. Old
baked English is not treated as Japanese source.

All three complete bodies pass actual Rafael RAM-backed native macro expansion,
original font painting, independent full pixels, glyph order, first/final letters,
cell bounds and guarded input/output regions. The full preview sheet was viewed.
Ruff passes. Their complete encoded bodies need62,57,41 bytes versus38,44,34-byte
old slots. They require catalog/relocation capacity; no shortened fallback is used.

## Review ledger and held record

`work/analysis/name_source_review_v286/native_correction_proof.json` binds99
reviewed records to exact canonical/clean bytes, English and existing complete
native glyph evidence.96 retain their wording; the three corrected records have
new evidence.345 of the444 records remain to review, including the held one.

SC0B141R0107's clean first byte97 is presentation state; decoding it together
with the first Japanese text byte corrupts the displayed source transcription.
The body after that byte reads: 提督！ いや、FI総帥！ やりましょう！
パシャ軍を倒しましょう！. Current migration metadata lacks its spoken context.
Keep its bytes unchanged until the existing route-specific actor/preamble and
context evidence is resolved. Its army/forces wording also needs a source review;
no new translation or actor identity is asserted here.

## Integration status

New overrides are `translations/confirmed_name_editorial_v286.json`. They are not
yet applied to the83-catalog/361-fixed prototype. Complete source review, updated
allocation/copy/glyph checks and registered combined release remain pending.
No playable ROM changed; V275 remains latest playable. All18 plaques and variants
remain incomplete. Online-image translation exemption is preserved. Full graphics
goal stays active; revisit older record-based checks at actual completion.
