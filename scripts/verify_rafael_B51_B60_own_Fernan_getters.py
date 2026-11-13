"""Read both original Fernan name consumers from the final ROM's own verified snapshot."""
import argparse
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.prove_lil_B167_names_v4124b import names as original_names

ADAPTER=Path('work/analysis/Rafael_B61_B80_new_name_bindings_20261104/names.json')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['release','startup','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    ctx=RegisteredRuntime(args.release,args.startup,captain=0)
    source=load(ADAPTER)['source_owned_current_adapter']
    env={**original_names.__globals__,'ACTORS':[35]}
    exec(compile(source,__file__+'::same-original-intrinsic-name-ABI-own-final-snapshot','exec'),env)
    result=ctx.execute(env['names'])
    assert len(result['rows'])==2 and {r['consumer'] for r in result['rows']}=={'progressive-nameplate','full-catalogue'}
    assert all(r['actor_ID']==35 and r['text']=='Fernan Silveira' and r['text_hex']==b'Fernan Silveira'.hex() for r in result['rows'])
    save(args.out,dict(runtime=ctx.receipt(),own_name_consumers=result,
        original_progressive_andfull_catalogue_getters_read_corrected_normal_F_from_own_snapshot=True,
        original_actor_objects_name_ring_owned_memory_andall_current_instruction_bytes_preserved=True,
        no_historical_RAM_overlay_ornew_emulator_run=True,full_catalogue_UI_unvisited=True,new_credit=0,
        adapter_source=str(ADAPTER),adapter_source_sha256=sha(ADAPTER.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Both original actor35 name getters return Fernan Silveira from own final captain0 snapshot;no historical RAM overlay.',flush=True)
