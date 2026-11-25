"""Bind source/current name fields and both original consumers for a reviewed scope."""
import argparse
import inspect
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prove_lil_B167_names_v4124b import names
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B169_contextual_v1 import fields


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('current','references','out'):p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    current,reference=map(load,(a.current,a.references))
    runtime=current['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=runtime['captain'])
    assert ctx.receipt()==runtime
    target=NdsImage.open(current['current_ROM'])
    assert digest(current['current_ROM'])==current['current_ROM_sha256']
    assert target.read_file('/__arm9__.bin')==ctx.arm and target.read_file('/COMMON/MESFILE.DK4')==ctx.common
    if current['current_ROM_sha256']!=ctx.release['candidate_sha256']:
        assert current['exact_native_context_reuse']['target_candidate_sha256']==current['current_ROM_sha256']
        assert current['exact_native_context_reuse']['complete_ARM9_font_payload_andCOMMON_exact']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    actors=sorted(r['actor_ID'] for r in reference['records'])
    assert len(actors)==len(set(actors)) and all(i in range(207) for i in actors)
    source=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in ACTORS:',
        "            print(dict(actor=ident,consumer=kind,text=value,rings=len(rings),writes=len(writes)),flush=True)":"            assert value == data.decode('cp932')",
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact=True':
            'all_requested_original_consumers_and_owned_or_readonly_memory_paths_exact=True',
    })
    env={**names.__globals__,'ACTORS':actors}
    exec(compile(source,__file__+'::unchanged-native-getters-and-memory-guards-scoped-actors','exec'),env)
    result=ctx.execute(env['names'])
    assert len(result['rows'])==2*len(actors)
    records=[]
    for original in reference['records']:
        actor=original['actor_ID'];bound=fields(actor,clean,ctx)
        assert bound==original['source_andcurrent_fields']
        forms=[r for r in result['rows'] if r['actor_ID']==actor]
        assert {r['consumer'] for r in forms}=={'progressive-nameplate','full-catalogue'}
        records.append(dict(actor_ID=actor,source_andcurrent_fields=bound,current_consumers=forms,
            source_andcurrent_reference_provenance=str(a.references),
            source_andcurrent_reference_sha256=digest(a.references),
            natural_name_localization_andnative_planes_still_pending=True))
    save(a.out,dict(records=records,scoped_actors=len(actors),original_native_name_getters=2*len(actors),
        runtime=runtime,target_candidate=current['current_ROM'],target_candidate_sha256=current['current_ROM_sha256'],
        complete_name_runtime_andfont_dependencies_exact=True,
        own_snapshot_reuse_not_new_gameplay=True,all_original_name_memory_guards_pass=True,
        no_global207_name_orfull_catalogue_UI_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in (a.current,a.references,Path(__file__))}))
    for row in records:
        if row['actor_ID'] in (55,56,57,151,153):
            print(row['actor_ID'],[(r['consumer'],r['text']) for r in row['current_consumers']])
    print(f'{len(actors)} actor references/{2*len(actors)} original name consumers; no fresh gameplay or name-plane approval.')


if __name__=='__main__':main()
