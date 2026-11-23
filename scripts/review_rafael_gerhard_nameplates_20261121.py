"""Confirm the six dialogue nameplates in the Gerhard recruitment exchange."""

from inspect import getsource

from scripts import review_rafael_east_asia_nameplates_20261121 as template
from scripts import stage_rafael_gerhard_tutorial_20261121 as stage
from scripts import verify_rafael_gerhard_tutorial_20261121 as display
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROOF = stage.ROOT / "speaker_labels.json"
NOTES = {
    0: "Rafael Castor is the approved full name. Claudio supplies both original name substitutions in the introduction.",
    4: "Janus Pasar identifies the navigator who gathers the local lead and asks why Vels was taken in.",
    5: "Claudio Manaus matches his complete self-introduction. His nickname Clau is used when Rafael speaks to him.",
    16: "Gerhard Adernkatz matches both the local directions and Claudio's formal introduction. The title is spoken where the source gives it.",
    82: "Shopkeeper is the established caption for the recurring character who hints at the retired navigator's whereabouts.",
    162: "Boy preserves the original speaking role of the character who gives directions.",
}
source = checked_text(getsource(template.main), {
    'selectors = {r["source_selector"] for r in review["records"]}':
        'selectors = {r["source_selector"] for r in review["records"] if r["kind"] == "progressive"}',
})
scope = vars(template) | globals()
exec(compile(source, __file__ + "::scope-six-nameplates", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
