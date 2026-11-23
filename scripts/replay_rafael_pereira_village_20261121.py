"""Sample the revised exchanges and the donation modal after original New Game initialization."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_spain_20261121 as prior
from scripts import stage_rafael_pereira_village_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay_v2"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
SEQUENCE = (
    (61, 107), (61, 113), (61, 122), (61, 136),
    (62, 5), (62, 23), (62, 34),
    (63, 55), (63, 79), (63, 92), (63, 113), (63, 146), (63, 179),
    (64, 91), (64, 95), (64, 126), (64, 206), (64, 295), (64, 340), (64, 352),
    (64, 355), (64, 439), (64, 485),
)
INPUT = [(4000 + i * 300, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 255 for frame, _ in INPUT[:-1]), END - 1)


source = checked_text(getsource(prior.replay), {
    '    group, = proof["groups"]': '    groups = {group["block"]: group for group in proof["groups"]}',
    '    opening, scene = (bank.blocks[i] for i in (44, 60))': '    opening = bank.blocks[44]',
    '''    assert opening[:4] == scene[:4] and opening[6:8] == scene[6:8]
    assert native.digest(scene) == group["after"]
    commands = {ident: cmd for cmd in group["commands"] for ident in cmd["record_ids"]}''':
        '''    for block_id, group in groups.items():
        scene = bank.blocks[block_id]
        assert opening[:4] == scene[:4] and opening[6:8] == scene[6:8]
        assert native.digest(scene) == group["after"]''',
    '''    for item in SEQUENCE:
        ident = item if isinstance(item, str) else f"DK4_MES_B60_R{item:04d}"
        command = commands[ident]''':
        '''    for block_id, item in SEQUENCE:
        ident = f"DK4_MES_B{block_id}_R{item:04d}"
        scene = bank.blocks[block_id]
        command, = [c for c in groups[block_id]["commands"] if c["record_ids"] == [ident]]''',
    '        assert command["word"] == (0x2100 if isinstance(item, str) else 0x4000)':
        '        assert command["word"] == 0x4000',
    'dict(ids=command["record_ids"], word=command["word"], fixture_offset=len(logical),':
        'dict(ids=command["record_ids"], block=block_id, word=command["word"], fixture_offset=len(logical),',
    '    terminal = group["commands"][-1]': '    terminal = groups[64]["commands"][-1]',
    '"Rafael_Spain_Choices_RESEARCH_ONLY.nds"': '"Rafael_Pereira_Village_RESEARCH_ONLY.nds"',
    'base.load(prior.INPUTS)': 'base.load(prior.prior.INPUTS)',
    'harness = prior.release_checks.template.games.harness': 'harness = prior.prior.release_checks.template.games.harness',
    'original_menu_objects_copied_byte_exact=True,\n        original_relationship_and_choice_branches_unexecuted=True':
        'original_speech_commands_copied_byte_exact=True,\n        original_scene_branches_unexecuted=True',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::selected-score-replay", "exec"), scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("replay", "startup", "patch"))
    case = parser.parse_args().check
    if case == "replay":
        scope["replay"]()
    else:
        template = prior.prior.release_checks.template
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
