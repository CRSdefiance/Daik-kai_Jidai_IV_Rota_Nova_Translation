"""Verify the reader-visible names and roles for the recruitment and sail batch."""

from types import SimpleNamespace

from scripts import review_hodram_midroute_nameplates_20261123 as prior
from scripts import stage_hodram_recruitment_and_sails_20261123 as stage

PROOF = stage.ROOT / "speaker_roles.json"
NOTES = {
    1: "Keep Hodram Bergstrom. Captain and admiral appear as the context calls for them within speech.",
    4: "Keep Janus Pasar for the crew member who acknowledges the sail explanation.",
    6: "Keep Julio Erneco for the conditional assessment of Angelo's trade advice.",
    7: "Keep Cristina Erneco. Her dancing and fencing are expressed within the conversation.",
    13: "Keep Cesare Tony for the crew member who comments on the lesson.",
    15: "Keep Angelo Puccini. His introduction gives the same full name as his header.",
    16: "Keep Gerhard Adernkatz for the officer who duels with Angelo.",
    17: "Keep Al Shin in the header and Al in his short self-introduction.",
    18: "Keep Charles Rochefort in the header and the separate native catalogue component Jean.",
    21: "Keep Ian Dukov. His profession as navigator is revealed in his own introduction.",
    23: "Keep Manuel Almeida for the crew member who explains the alignment of the masts.",
    92: "Keep Barkeep for the tavern worker directing Ian's service and taking Hodram's order.",
    96: "Keep Patron for the customer who pursues Ian. The label matches his introduction at the tavern.",
    109: "Keep Shipwright for the unnamed worker offering the lesson on sail rigs.",
    139: "Keep Priest for the officiant who explains the Map Keys and offers a blessing.",
    148: "Keep Guildmaster for Al's employer at the guild.",
    152: "Keep Sailor for the companion in the group confronting Ian.",
    164: "Keep Man for the anonymous person who comments on Ian in the tavern.",
    165: "Keep Woman for the anonymous person who points out Ian in the tavern.",
}
scope = prior.scope | dict(PROOF=PROOF, NOTES=NOTES, parent=stage.parent,
    stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
    display=SimpleNamespace(PROOF=stage.NATIVE), assets=stage.established.display.ASSETS)
exec(compile(prior.source, __file__ + "::native-speaker-fields", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
