"""Check the fifteen localized names and roles used in Rafael's midroute exchanges."""

from inspect import getsource
from types import SimpleNamespace

from scripts import review_rafael_east_asia_nameplates_20261121 as audit
from scripts import stage_rafael_midroute_exchanges_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text

PROOF = stage.ROOT / "speaker_roles.json"
NOTES = {
    0: "Keep Rafael Castor and the captain name substitution. Julio and Claudio address the player through the native field.",
    4: "Keep Janus Pasar. His discussion of a lost telescope supplies no different rank or title.",
    5: "Keep Claudio Manaus in headings and his familiar Clau nickname in Rafael's and Arcadius's replies.",
    6: "Keep Julio Erneco. Cristina's grandfather is a family relationship expressed by the dialogue.",
    8: "Keep Arcadius Eudoxios in the public nameplate and Eirene in the separate catalogue field. The asides support the distinction.",
    12: "Keep Yukihisa Shiraki in the nameplate and Genjo in the separate catalogue field. Rafael recognizes Yukihisa for his tip.",
    14: "Keep Emilio Ferog. Rafael repeats Emilio's given name when quoting the invitation to eat.",
    18: "Keep Charles Rochefort in the nameplate and Jean in the separate catalogue field. His scientific speech needs no professional title.",
    22: "Keep Samwell Khan in the nameplate and da in the separate catalogue field. Rafael recognizes the familiar rumor pitch.",
    75: "Keep Hans Letzel. His years of research are stated in dialogue without giving him an office.",
    114: "Port Worker suits the dock attendant who identifies amber and passes along a local rumor.",
    137: "Senior Monk preserves the source's senior religious role without assigning the monk a personal name or specific office.",
    160: "Villager identifies the person entrusting the inherited lamp and does not presume a denomination.",
    177: "Sect Leader fits the founder or leader who claims a revelation and gives orders to the group.",
    178: "Follower reads naturally for the believer who answers the Sect Leader's calls.",
}
source = checked_text(getsource(audit.main), {
    '    dependencies = rendered["initialized_dependencies"]\n'
    '    ctx = native.RegisteredRuntime(dependencies["release_proof"], dependencies["startup_proof"], captain=0)':
        '    previous = base.load(parent.RELEASE)\n'
        '    ctx = native.RegisteredRuntime(parent.RELEASE, previous["own_registered_startup"], captain=3)',
    'f\'for ident in {sorted(selectors)}:\'': 'f\'for ident in {sorted(selectors - {0})}:\'',
    '    with redirect_stdout(StringIO()):\n        executed = ctx.execute(scope["names"])':
        '    with redirect_stdout(StringIO()):\n'
        '        executed = ctx.execute(scope["names"])\n'
        '    context0 = base.load(stage_context)["previous_initialized_rafael_context"]\n'
        '    boot, identity = map(Path, (context0["path"], context0["identity"]))\n'
        '    assert base.digest(boot) == context0["sha256"] and base.digest(identity) == context0["identity_sha256"]\n'
        '    rafael = native.RegisteredRuntime(identity, boot, captain=0)\n'
        '    assert rafael.image.read_file("/GRP/KANJI.FNT") == image.read_file("/GRP/KANJI.FNT")\n'
        '    rafael_code = checked_text(script, {f"for ident in {sorted(selectors - {0})}:": "for ident in [0]:", "len(provider.executed_current)": "sorted(provider.executed_current)"})\n'
        '    exec(compile(rafael_code, __file__ + "::rafael-name-getters", "exec"), scope)\n'
        '    with redirect_stdout(StringIO()):\n'
        '        executed["rows"].extend(rafael.execute(scope["names"])["rows"])\n'
        '    live = base.load(live_receipt)\n'
        '    assert live["candidate_sha256"] == candidate\n'
        '    assert any(r["speaker"] == "Rafael Castor" and r["exact_complete_body_mask"] for r in live["observations"])',
    'runtime_dependencies=ctx.receipt(), records=receipts,':
        'runtime_dependencies=ctx.receipt(), rafael_initialized_dependency=rafael.receipt(),\n'
        '                         current_rafael_nameplate_gameplay_sha256=base.digest(live_receipt), records=receipts,',
    'known["full_catalogue"]]': 'known["full_catalogue"]], (ident, getters)',
    'display.display.ASSETS': 'assets',
    'selectors = {r["source_selector"] for r in review["records"]}':
        'selectors = {r["source_selector"] for r in review["records"]} - {254}',
    'native_getters=getters, decision="retention", localization_note=NOTES[ident])':
        'native_getters=getters, decision="retention", localization_note=NOTES[ident],\n'
        '                             review=dict.fromkeys(("source","context","localization","naturalness","formatting"), True))',
})
scope = vars(audit) | dict(base=stage.base, native=stage.native, PROOF=PROOF, NOTES=NOTES, parent=stage.parent,
    stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
    display=SimpleNamespace(PROOF=stage.NATIVE), assets=stage.established.display.ASSETS,
    stage_context=stage.established.display.build.parent.display.PROOF,
    live_receipt=stage.ROOT / "focused_gameplay/verified_gameplay.json")
exec(compile(source, __file__ + "::native-speaker-fields", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
