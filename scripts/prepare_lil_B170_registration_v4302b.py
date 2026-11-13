"""Keep the early list-root traversal failure and bind JSON arrays as leaf inputs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B170_registration_tools_v4302b')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/register_lil_B170_v4302.py', 'scripts/register_lil_B170_v4302b.py', {
        'lil_B170_registration_v4302': 'lil_B170_registration_v4302b',
        'build_integrated_release_v4302.tmp': 'build_integrated_release_v4302b.tmp',
        '        value = read(path)\n': '        value = read(path)\n        if not isinstance(value, dict):\n            continue\n',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool,
        explanation='The first dependency walk reached a hash-bound controller schedule whose JSON root is an array. Arrays are valid dependencies but contain no top-level evidence/dependencies object to traverse. Keep their hashes and traverse proof objects only. The failed predecessor stopped before creating its output root,config,registry or builder mutation.',
        no_compiler_guard_or_proof_scope_changed=True, positive_negative_and_registration_pending=True, full_goal_complete=False))
