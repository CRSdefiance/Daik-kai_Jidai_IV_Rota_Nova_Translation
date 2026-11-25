"""Review and verify the speaking labels in Rafael's Spain and London exchanges."""

from inspect import getsource

from scripts import review_rafael_east_asia_nameplates_20261121 as precedent
from scripts import stage_rafael_spain_london_20261121 as stage
from scripts import verify_rafael_spain_london_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROOF = stage.ROOT / "speaker_labels.json"
NOTES = {
    0: "Rafael Castor is the approved name. His introduction preserves both substitutions.",
    4: "Janus Pasar's complete personal name identifies the crew member watching the bullfight.",
    5: "Claudio Manaus remains consistent with the other crew exchanges. His joking manner comes from his lines.",
    6: "Julio Erneco identifies Cristina's grandfather. The verified relationship belongs in their speech, not the nameplate.",
    7: "Cristina Erneco agrees with her given name in the dialogue and the separate source family-name field.",
    14: "Emilio Ferog is the same name he supplies when Rafael recruits him.",
    15: "Angelo Puccini identifies the speaker of the confident aside without adding a title.",
    79: "Mivor Genz is the approved full name he supplies when meeting Julio.",
    82: "Shopkeeper remains the established label for the recurring town character now in the crowd.",
    95: "Patron works for this recurring spectator. It does not force the current location to be a tavern.",
    104: "Trader remains the established role of the spectator who announces the main act.",
    113: "Port Worker identifies the known town character, whose line here is a spectator's cheer.",
    147: "Guildmaster identifies the town's guild leader among the crowd.",
    162: "Boy comes from the original category and agrees with the textual role in the three speakerless panels.",
    167: "Lady preserves the source's general role label. Her relationship to the boy comes from what she says.",
}


source = checked_text(getsource(precedent.main), {
    'selectors = {r["source_selector"] for r in review["records"]}':
        'selectors = {r["source_selector"] for r in review["records"] if r["source_selector"] != 254}',
})
scope = vars(precedent) | globals() | {"precedent": precedent.precedent}
exec(compile(source, __file__ + "::scoped-nameplate-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
