"""Verify glyphs, controls, choices and companion slots for the rescue and lesson batch."""

from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import stage_rafael_rescue_and_lessons_20261121 as stage
from scripts import verify_rafael_ruins_and_proof_20261121 as template
from scripts import verify_rafael_sailing_lisbon_gameplay_20261121 as lisbon
from scripts.source_locked_derivation_v5118 import checked_text


base, native, display, town = stage.base, stage.native, template.display, template.town
ROOT = stage.ROOT / "native_display"
PROOF, NAMES = ROOT / "native_display.json", stage.ROOT / "speaker_labels.json"
REFERENCE = stage.ROOT.with_name("staged_v2")
PATH = template.PATH


def audit_company_name():
    function = display.display.paragraph
    source = checked_text(getsource(function), {
        '{macro: example for macro in tokens}':
            '{macro: example + (" Co." if macro == "FO" and n == 16 else "") for macro in tokens}',
    })
    env = function.__globals__ | {"build": stage}
    exec(compile(source, __file__ + "::company-name", "exec"), env)
    return env["paragraph"]


def prior_lisbon(image, stored):
    receipt = base.load(lisbon.PROOF)
    assert receipt["natural_activation"] and receipt["original_Lisbon_departure_activation"]
    assert receipt["candidate_sha256"] == base.digest(lisbon.active.ROM)
    groups = {item["block"]: item for item in stored["groups"]}
    group = groups[128]
    old = base.NdsImage.open(lisbon.active.ROM)
    dependency_paths = [*display.ASSETS, "/data/EV0.DK4"]
    assert all(old.read_file(p) == image.read_file(p) for p in dependency_paths)
    old_data = native.IlnkContainer.parse(old.read_file(PATH)).blocks[128]
    assert native.digest(old_data) == group["before"]
    commands = {key: cmd for cmd in group["commands"] for key in cmd["record_ids"]}
    unchanged, revised = [], []
    for panel in receipt["panels"]:
        ident, ref = panel["id"], panel["registered_reference"]
        command = commands[ident]
        before = bytes.fromhex(command["current"])
        body = bytes.fromhex(ref["exact_stored_hex"])
        offset = ref["command_offset"]
        assert old_data[offset:offset + len(before)] == before and before[5:5+len(body)] == body
        if command["current"] == command["stored"]:
            unchanged.append(ident)
        else:
            revised.append(ident)
    assert len(unchanged) + len(revised) == 44
    assert len(revised) == 4
    return dict(path=str(lisbon.PROOF), sha256=base.digest(lisbon.PROOF), runtime_and_event_dependencies_exact=dependency_paths,
                exact_prior_observed_record_ids=unchanged, revised_since_prior_play=revised,
                unvisited_ids=receipt["unobserved_records"], fresh_ordinary_play=False)


part_source = checked_text(getsource(template.parts), {
    'target[18:20] == current[18:20] == source[18:20] == b"\\0\\xd0"':
        'target[18:20] == current[18:20] == source[18:20] == bytes([0, rows[0]["source_selector"]])',
})
name_source = checked_text(getsource(template.verify_names), {
    '''    notes[135] = ("Officiant is the registered role for the guardian of the Vishnu temple. The original short "
                  "name and this exchange give no particular priestly rank.")''':
    '''    notes[170] = ("Mysterious Old Man is the established caption for the unnamed man in the rescue. "
                  "His own words establish that the boy is his grandson and that he earned the governor's reward.")''',
    'and r["source_selector"] not in (207, 208)': 'and r["source_selector"] < 207',
})

main_source = checked_text(getsource(template.main), {
    '    audits = prior.prior.precedent.name_audit()': '    audits = audit_company_name()',
    'len(entries) == 255 and not rows and len(menus) == 4 and fe_count == 22 and len(style_objects) == 2':
        'len(entries) == 351 and not rows and len(menus) == 5 and fe_count == 15 and len(style_objects) == 6',
    '        previous_native_proof=str(previous_native), reused_record_ids=reused,':
        '        previous_native_proof=str(previous_native), reused_record_ids=reused,\n'
        '        prior_ordinary_sailing_coverage=prior_lisbon(image, stored),',
    '"final_speech", 216': '"company_speech", 216',
    '"final_speakerless", 228': '"company_speakerless", 228',
    '12 captions and both companion objects.': 'ten captions and six companion objects.',
})
scope = vars(template) | globals() | {"prior": template.prior}
for code in (part_source, name_source, main_source):
    exec(compile(code, __file__ + "::display", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()

