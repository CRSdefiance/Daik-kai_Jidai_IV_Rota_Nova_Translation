"""Reload the new archive and reuse exact parent modes outside its owned changed blocks."""
from scripts.check_rafael330_loaders_v1 import source as previous, parent_adapter
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    "    parser.add_argument('--out', type=Path, required=True)":
        "    for name in ['out','reconstruction','prior-modes']:\n        parser.add_argument('--'+name,type=Path,required=True)",
    "rebuild_path = Path('work/analysis/Rafael330_stored_consumer_inputs_20261105/native_consumer_reconstruction.json')":
        'rebuild_path = args.reconstruction',
    "latest_path=Path('work/analysis/Rafael_B61_B80_loaders_v12_20261104/verification.json')": 'latest_path=args.prior_modes',
    'assert changed == {81,82,83,84}': "assert changed == set(rebuilt['changed_blocks'])",
    "'pending-Rafael330-research'": "'pending-qualified-Rafael-research'",
    'assert len(fresh) == 8 and len(reused) == 678': 'assert len(fresh) == 2*len(changed) and len(reused) == 2*(len(blocks)-len(changed))',
    'fresh_parent_cases=8': 'fresh_parent_cases=len(fresh)',
    'exact_reused_parent_cases=678': 'exact_reused_parent_cases=len(reused)',
    "print('343 whole native loads/cache hits;eight fresh and678 exact reused parent cases pass.')":
        "print(dict(native_loads=len(blocks),fresh_parent_cases=len(fresh),exact_reused_parent_cases=len(reused)),flush=True)",
})
exec(compile(source, __file__+'::same-native-load-guards-and-exact-qualified-parent-case-reuse', 'exec'), globals())
