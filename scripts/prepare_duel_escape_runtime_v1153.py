"""Prepare the same-allocation escape-speech membership successor."""
from pathlib import Path
from scripts import duel_escape_runtime_v1152 as runtime
from scripts.probe_duel_cache_scope_v1150 import PLAN_PATH
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/duel_escape_runtime_v1153')


def main():
    assert not ROOT.exists()
    source_plan = read(PLAN_PATH)
    arm = Path(source_plan['target_ARM9']).read_bytes()
    assert sha(arm) == source_plan['target_ARM9_sha256']
    target, plan = runtime.apply(arm)
    ROOT.mkdir(parents=True)
    path = ROOT/'ARM9_RESEARCH_ONLY.bin'
    path.write_bytes(target)
    save(ROOT/'runtime_plan.json', {**plan, 'research_ARM9': str(path),
        'source_cache_payload_plan': str(PLAN_PATH), 'source_cache_payload_plan_sha256': sha(PLAN_PATH.read_bytes()),
        'runtime_module_sha256': sha(Path(runtime.__file__).read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Two exact native escape tables added; same212-byte public bank, no executable or memory growth.')


if __name__ == '__main__':
    main()
