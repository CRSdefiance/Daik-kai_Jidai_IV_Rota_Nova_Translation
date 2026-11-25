"""Exercise Rafael's training panels and Hodram's native fog choices."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType

from scripts import replay_caves_offshore_monk_20261118 as fog
from scripts import replay_embedded_story_roles_20261115 as opening
from scripts import replay_rafael_mosque_20261118 as rafael
from scripts import stage_warrior_village_handovers_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
ROOT = stage.ROOT / "trial"
ROM = ROOT / "Rafael_Warrior_Trial_RESEARCH_ONLY.nds"
SETUP, LIVE = ROOT / "fixture.json", ROOT / "verified.json"
EXCERPTS = (
    (336, (5, 9, 13, 18, 21, 26, 30, 34, 39, 42, 46, 51, 55, 59, 109, 112, 116, 121, 125, 130, 134)),
    (337, (29, 36, 40, 43, 47)),
    (338, (106, 113, 117, 122)),
)
LAST = 11201
trial_scope = rafael.scope | globals()
for source, tag in ((rafael.prep, "trial-speech-commands"), (rafael.audit, "trial-and-native-notices")):
    exec(compile(source, __file__ + "::" + tag, "exec"), trial_scope)
trial = FunctionType(rafael.capture.__code__, trial_scope)
startup = FunctionType(rafael.startup.__code__, trial_scope)

HODRAM_ROOT = stage.ROOT / "mist"
HODRAM_ROM = HODRAM_ROOT / "Hodram_Fog_RESEARCH_ONLY.nds"
HODRAM_SETUP = HODRAM_ROOT / "fixture.json"
mist_scope = vars(fog) | {
    "ROOT": HODRAM_ROOT, "ROM": HODRAM_ROM, "SETUP": HODRAM_SETUP, "stage": stage,
    "FIRST": 516, "LAST": 7701, "OPENING": opening.INPUTS,
}
source = checked_text(getsource(fog.prepare_fog), {
    'path = "/data/SC0.DK4"': 'path = "/data/SC1.DK4"',
    'g["block"] == 332': 'g["block"] == 316',
    'host, block = bank.blocks[44], bank.blocks[332]': 'host, block = bank.blocks[42], bank.blocks[316]',
    'len(guest) == 30': 'len(guest) == 41',
    'host[:40]': 'host[:42]',
    '    assert len(actual) == 10 + len(guest)':
        '''    prefix, _ = inventory(image.read_file(native.ARM), host)
    count = sum(c["offset"] < 42 for c in prefix)
    assert len(actual) == count + len(guest)
    assert [c["word"] for c in actual[:count]] == [c["word"] for c in prefix[:count]]''',
    'actual[10:]': 'actual[count:]',
    '- start + 40': '- start + 42',
    'bank.blocks[44]': 'bank.blocks[42]',
    '    previous = rafael.scope["precedent"].stage.CAPTURE\n    schedule = base.load(previous)["scripted_input_schedule"] + [':
        '    schedule = [event for event in base.load(OPENING) if event["start"] <= 2200] + [',
    "initialized_Rafael=True": "initialized_Hodram=True",
})
exec(compile(source, __file__ + "::original-Hodram-fog-commands", "exec"), mist_scope)
mist = FunctionType(rafael.capture.__code__, rafael.scope | mist_scope)

if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare_trial", "trial", "verify_trial", "prepare_mist", "mist", "startup"))
    actions = {
        "prepare_trial": trial_scope["prepare"], "trial": trial, "verify_trial": trial_scope["verify"],
        "prepare_mist": mist_scope["prepare_fog"], "mist": mist, "startup": startup,
    }
    actions[parser.parse_args().action]()
