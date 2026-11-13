"""Reuse exact latest parent cases; reload the current archive and changed blocks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/check_pending_scene_loaders.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    parser.add_argument('--out', type=Path, required=True)":
    "    for arg in ['reconstruction','previous','out']:parser.add_argument('--'+arg,type=Path,required=True)",
    "    rebuild_path = Path('work/analysis/Hodram_B61_B70_stored_20261101/reconstruction.json')":
    "    rebuild_path = args.reconstruction",
    '    rebuilt, prior = load(rebuild_path), load(prior_path)':
    """    rebuilt, prior = load(rebuild_path), load(prior_path)
    previous=load(args.previous)
    assert previous['prior_sha256']==sha(prior_path.read_bytes())
    prior={**prior,'parent_mode_proof':previous['modes'],'parent_mode_sha256':previous['modes_sha256']}""",
    '    assert changed == set(range(61, 71))':
    "    assert changed=={g['block'] for g in rebuilt['groups']}",
    '    assert len(fresh) == 20 and len(reused) == 630':
    '    assert len(fresh)==2*len(changed) and len(reused)==2*(len(blocks)-len(changed))',
    'fresh_parent_cases=20':'fresh_parent_cases=len(fresh)',
    'exact_reused_parent_cases=630':'exact_reused_parent_cases=len(reused)',
    '        prior=str(prior_path), prior_sha256=sha(prior_path.read_bytes()),':
    "        prior=str(prior_path), prior_sha256=sha(prior_path.read_bytes()),previous=str(args.previous),previous_sha256=sha(args.previous.read_bytes()),",
    "    print('325 whole native loads/cache hits;20 fresh and630 exact reused parent cases pass.')":
    "    print(dict(whole_native_loads=325,fresh_parent_cases=len(fresh),exact_reused_parent_cases=len(reused)))",
})
exec(compile(source,__file__+'::exact-parent-case-reuse','exec'),globals())
