"""Check fresh startup on the source-owned Ancient Map Hint correction."""

import argparse
from types import FunctionType

from scripts import run_diplomatic_outcome_startup_v2 as replay
from scripts import stage_ancient_map_hint_label_v1 as stage
from scripts import verify_setup_save_equipment_v1 as startup


base = stage.base
ROOT, ROM = stage.ROOT, stage.ROM
PROOF = ROOT / 'startup_input.json'
BOOT = ROOT / 'own_startup_verification.json'
BIOGRAPHIES = stage.parent.stage.ROOT


def run():
    proof = base.load(stage.PROOF)
    assert base.digest(ROM) == proof['candidate_sha256']
    assert base.digest(stage.parent.ROM) == proof['parent_sha256']
    base.save(PROOF, dict(research_ROM_sha256=proof['candidate_sha256'],
        registered_input=dict(candidate_sha256=proof['parent_sha256'])))
    FunctionType(replay.main.__code__, vars(replay) | dict(EVIDENCE=PROOF, ROM=ROM,
        STARTUP=ROOT / 'own_startup', PRIOR=BIOGRAPHIES / 'own_startup'))()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    if parser.parse_args().verify:
        FunctionType(startup.verify_startup.__code__, vars(startup) | globals())()
    else:
        run()
