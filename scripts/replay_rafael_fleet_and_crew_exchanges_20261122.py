"""Verify Rafael's revised dialogue, native modal panels, and return to port."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_charlotte_and_maria_20261122 as prior
from scripts import review_rafael_east_asia_nameplates_20261121 as role_audit
from scripts import stage_rafael_fleet_and_crew_exchanges_20261122 as stage
from scripts import verify_rafael_athens_and_maria_crew_20261122 as modal
from scripts.source_locked_derivation_v5118 import checked_text


base, native, gameplay = stage.base, stage.native, prior.gameplay
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
ROLES = stage.ROOT / "speaker_roles.json"
SAMPLE = {0: ((74, 5), (74, 8), (74, 12), (74, 16), (74, 24), (81, 51), (81, 106), (81, 118), (81, 159), (81, 224),
    (83, 55), (83, 101), (83, 104), (83, 111), (83, 114), (83, 117), (83, 120), (83, 123),
    (83, 226), (83, 255), (83, 307), (87, 93), (87, 210), (90, 32), (97, 58))}
RUNTIME_VALUES = {}
scope = prior.scope | globals()
for name in ("receipt", "report_path", "run_file", "play"):
    original = prior.scope[name]
    scope[name] = FunctionType(original.__code__, scope)
fixture_source = checked_text(prior.fixture_source, {
    "Rafael_Charlotte_And_Maria_FOCUSED_ONLY.nds": "Rafael_Fleet_And_Crew_FOCUSED_ONLY.nds",
})
exec(compile(fixture_source, __file__ + "::focused-fixture", "exec"), scope)


def report(run):
    return scope["report_path"](int(run))


modal_source = checked_text(getsource(modal.check_modal), {
    'len(records) == 10 and sum(r["second_page"] for r in records) == 2':
        'len(records) == 4 and not any(r["second_page"] for r in records)',
    'Verified all ten modal pages, including both original two-page Maria sequences.':
        'Verified all four original Rafael modal panels.',
})
modal_scope = vars(modal) | {"stage": stage}
exec(compile(modal_source, __file__ + "::modal-verification", "exec"), modal_scope)

role_notes = {
    82: "Keep Shopkeeper for the everyday town role reused by the spectator heckling in the arena.",
    83: "Keep Shopkeeper for the merchant who reports the gathering fleets before Seville.",
    95: "Keep Patron for the spectator enjoying Emilio's performance. There is no extra title in the scene.",
    104: "Keep Trader for the trading-house worker who asks about the fight off Seville.",
    113: "Keep Port Worker for the dock attendant who gives the warning and relays the summons.",
    147: "Keep Guildmaster for the guild leader who tells Rafael to wait until the crew is ready.",
    158: "Keep Sailor in the speaking header for Kurushima's seagoing subordinate and Retainer in the catalogue for the broader source role.",
    162: "Keep Boy when the rescued child speaks, consistent with the Boy cue in his speakerless panic panels.",
    167: "Keep Lady for the woman asking help for her son and thanking the rescuers. The label gives her no specific title.",
}
roles_source = checked_text(getsource(role_audit.main), {
    '    dependencies = rendered["initialized_dependencies"]\n'
    '    ctx = native.RegisteredRuntime(dependencies["release_proof"], dependencies["startup_proof"], captain=0)':
        '    release = base.load(parent.RELEASE)\n'
        '    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)',
    'display.display.ASSETS': 'assets',
    'selectors = {r["source_selector"] for r in review["records"]}':
        'selectors = {r["source_selector"] for r in review["records"]} & NOTES.keys()',
    'native_getters=getters, decision="retention", localization_note=NOTES[ident])':
        'native_getters=getters, decision="retention", localization_note=NOTES[ident],\n'
        '                             review=dict.fromkeys(("source","context","localization","naturalness","formatting"), True))',
})
roles_scope = vars(role_audit) | dict(base=base, native=native, PROOF=ROLES, NOTES=role_notes, parent=stage.parent,
    stage=SimpleNamespace(OUTPUT=stage.REVIEW, PROOF=stage.PROOF, ROM=stage.ROM),
    display=SimpleNamespace(PROOF=stage.NATIVE), assets=stage.established.display.ASSETS)
exec(compile(roles_source, __file__ + "::role-verification", "exec"), roles_scope)


def formatting():
    FunctionType(prior.formatting.__code__, vars(prior) | globals())()
    modal_scope["check_modal"]()
    roles_scope["main"]()


verify_source = checked_text(getsource(prior.verify), {
    'proof, display, manuscript = map(base.load, (stage.PROOF, stage.NATIVE, stage.REVIEW))':
        'proof, display, manuscript, modal_proof = map(base.load, (stage.PROOF, stage.NATIVE, stage.REVIEW, stage.FE_PROOF))',
    'candidate == proof["candidate_sha256"] == display["candidate_sha256"]':
        'candidate == proof["candidate_sha256"] == display["candidate_sha256"] == modal_proof["candidate_sha256"]',
    '    pictures, observations = [], []':
        '    pictures, observations = [], []\n'
        '    system = {item["id"]: item for item in modal_proof["records"]}',
    '        if row["layouts"]:\n            assert not values\n            page, = row["layouts"][0]["pages"]':
        '        if ident in system:\n'
        '            assert command["exact_command_hex"] == system[ident]["exact_command_hex"]\n'
        '            page = None\n'
        '        elif row["layouts"]:\n'
        '            assert not values\n'
        '            layout = row["layouts"][0]\n'
        '            if layout["scope"] == "registered default":\n'
        '                body = bytes.fromhex(row["body_hex"])[1:]\n'
        '                values = {key: display["default_names"]["0"][key] for key in ("FI", "FA", "FO") if key.encode() in body}\n'
        '                assert values\n'
        '            page, = layout["pages"]',
    '        assert gameplay.mask_check(bytes.fromhex(page["native_plane_hex"]), 216, image), (ident, frame)\n'
    '        speaker = labels[ident]\n'
    '        gameplay.glyphs(names, image, speaker, (16, 277), gameplay.LABEL_COLOR, 226)':
        '        speaker = labels[ident]\n'
        '        if page is None:\n'
        '            assert gameplay.mask_check(bytes.fromhex(system[ident]["physical_plane_hex"]), 228, image), (ident, frame)\n'
        '            assert not any(pixel == gameplay.LABEL_COLOR for pixel in image.crop((16,277,226,288)).get_flattened_data())\n'
        '        else:\n'
        '            assert gameplay.mask_check(bytes.fromhex(page["native_plane_hex"]), 216, image), (ident, frame)\n'
        '            gameplay.glyphs(names, image, speaker, (16, 277), gameplay.LABEL_COLOR, 226)',
    '    assert len(observations) == len(SAMPLE[0])':
        '    assert len(observations) == len(SAMPLE[0]) and system.keys() <= {r["id"] for r in observations}',
    "rafael_charlotte_and_maria_gameplay_": "rafael_fleet_and_crew_gameplay_",
    "focused speech holds, default name substitutions, and the host exit.":
        "focused holds, including four original modal panels, default names and the host exit.",
})
verify_scope = vars(prior) | globals()
exec(compile(verify_source, __file__ + "::gameplay-verification", "exec"), verify_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "formatting", "verify"))
    action = cli.parse_args().action
    if action == "replay":
        scope["fixture"](0)
        scope["play"](0)
    elif action == "formatting":
        formatting()
    else:
        verify_scope["verify"]()
