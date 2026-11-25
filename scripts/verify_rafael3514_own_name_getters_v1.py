"""Check both previously registered and new normal-width F names from own RAM."""
import argparse
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.prepare_rafael3514_Francisca_field_v1 import FIELD, digest
from scripts.prove_lil_B167_names_v4124b import names
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ('release', 'startup', 'out'):
        parser.add_argument('--'+arg, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    ctx = RegisteredRuntime(args.release, args.startup, captain=0)
    adapter = FIELD.parent/'native_getter_binding.json'
    source = load(adapter)['source_owned_current_adapter']
    expected = {35:'Fernan Silveira', 186:'Francisca'}
    env = {**names.__globals__, 'ACTORS':sorted(expected)}
    exec(compile(source, __file__+'::original-getters-own-final-snapshot', 'exec'), env)
    results = ctx.execute(env['names'])
    assert len(results['rows']) == 4
    for actor, text in expected.items():
        rows = [r for r in results['rows'] if r['actor_ID'] == actor]
        assert {r['consumer'] for r in rows} == {'progressive-nameplate','full-catalogue'}
        assert all(r['text'] == text and r['text_hex'] == text.encode('ascii').hex() for r in rows)
    save(args.out, dict(runtime=ctx.receipt(), own_name_consumers=results,
        both_name_getters_exact_for_actors_35_and_186=True,
        full_catalogue_UI_unvisited=True, no_historical_RAM_overlay=True, new_credit=0,
        adapter=str(adapter), adapter_sha256=digest(adapter)))
    print('Both original getters returned the complete registered Fernan Silveira and Francisca names.')


if __name__ == '__main__':
    main()
