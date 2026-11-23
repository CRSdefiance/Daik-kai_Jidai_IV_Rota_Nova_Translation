"""Bind the names and role labels used in the reviewed Hodram exchanges."""

from inspect import getsource
from types import SimpleNamespace

from scripts import review_rafael_east_asia_nameplates_20261121 as audit
from scripts import stage_hodram_midroute_followups_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text

PROOF = stage.ROOT / "speaker_roles.json"
NOTES = {
    1: "Keep Hodram Bergstrom for the speaking header and the native surname Escante uses. Admiral is his spoken office.",
    3: "Keep Maria Li for the negotiator in Sao Jorge. Her affiliation is supplied separately through FO.",
    6: "Keep Julio Erneco. He names his relationship to Cristina in speech.",
    9: "Keep Camille Overijssel in the nameplate and Camille where Hodram recognizes the visitor.",
    10: "Keep Xien Yan for Maria's companion who defends the townspeople.",
    12: "Keep Yukihisa Shiraki in the nameplate and the separate Genjo catalogue field. His interpretation does not make him a ninja.",
    15: "Keep Angelo Puccini. His teasing and Italian exclamation identify his voice without a role label.",
    16: "Keep Gerhard Adernkatz. His private advice is distinct from the admiral's decision.",
    18: "Keep Charles Rochefort in the nameplate and Jean in the separate catalogue field. His interest in science is expressed in his own words.",
    22: "Keep Samwell Khan in the nameplate and the separate da catalogue component. His familiar Peacock Mail speech matches the other route.",
    23: "Keep Manuel Almeida for the crew member who handles resupply advice.",
    43: "Keep Diogo Escante in the nameplate, with de in the separate catalogue field and the full name in the guildmaster's introduction.",
    58: "Keep Jorge Albacete for the man who warns Hodram to watch his mouth. The introduction gives him no new office.",
    114: "Port Worker fits the dock attendant who recognizes amber and relays the rumor.",
    139: "Priest fits the officiant who gives the sword and offers a blessing.",
    147: "Guildmaster is the role introducing Escante in the guild.",
    180: "Bandit fits the source role in the argument with Maria. The exchange gives no personal name.",
    198: "Keep Benazir as the name of the speaker who returns a favor with a lead about India.",
}
source = checked_text(getsource(audit.main), {
    '    dependencies = rendered["initialized_dependencies"]\n'
    '    ctx = native.RegisteredRuntime(dependencies["release_proof"], dependencies["startup_proof"], captain=0)':
        '    previous = base.load(parent.RELEASE)\n'
        '    ctx = native.RegisteredRuntime(parent.RELEASE, previous["own_registered_startup"], captain=3)',
    'display.display.ASSETS': 'assets',
    'selectors = {r["source_selector"] for r in review["records"]}':
        'selectors = {r["source_selector"] for r in review["records"] if r["source_selector"] < 207}',
    'known["full_catalogue"]]': 'known["full_catalogue"]], (ident, getters)',
    'native_getters=getters, decision="retention", localization_note=NOTES[ident])':
        'native_getters=getters, decision="retention", localization_note=NOTES[ident],\n'
        '                             review=dict.fromkeys(("source","context","localization","naturalness","formatting"), True))',
})
scope = vars(audit) | dict(base=stage.base, native=stage.native, PROOF=PROOF, NOTES=NOTES, parent=stage.parent,
    stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
    display=SimpleNamespace(PROOF=stage.NATIVE), assets=stage.established.display.ASSETS)
exec(compile(source, __file__ + "::native-speaker-fields", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
