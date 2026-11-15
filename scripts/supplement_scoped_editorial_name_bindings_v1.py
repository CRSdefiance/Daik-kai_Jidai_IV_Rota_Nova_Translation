"""Reuse exact scoped getter bindings andadd only newly resolved dynamic actors."""
import argparse
import inspect
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B169_contextual_v1 import fields, getter
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['names','roles','out']:
        parser.add_argument('--'+name,type=Path,required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    names, roles = map(load,[args.names,args.roles])
    receipt = names['runtime']
    assert receipt==roles['runtime']
    ctx = RegisteredRuntime(receipt['release_proof'],receipt['startup_proof'],captain=receipt['captain'])
    assert ctx.receipt()==receipt
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    records = deepcopy(names['records'])
    old_actors = {r['actor_ID'] for r in records}
    for row in records:
        assert fields(row['actor_ID'],clean,ctx)==row['source_andcurrent_fields']
        row['exact_reused_native_getter_binding'] = str(args.names)
    fresh = sorted({r['resolved_actor_ID'] for r in roles['native_roles']['rows']} - old_actors)
    assert fresh and all(0<=actor<207 for actor in fresh)
    code = checked_text(inspect.getsource(getter),{'for ident in [2,4,13,23,109]:':'for ident in FRESH:'})
    env = {**getter.__globals__,'FRESH':fresh}
    exec(compile(code,__file__+'::same-original-intrinsic-getters-fresh-dynamic-actors','exec'),env)
    result = ctx.execute(env['names'])
    assert len(result['rows'])==2*len(fresh)
    for actor in fresh:
        consumers = [r for r in result['rows'] if r['actor_ID']==actor]
        assert {r['consumer'] for r in consumers}=={'progressive-nameplate','full-catalogue'}
        records.append(dict(actor_ID=actor,source_andcurrent_fields=fields(actor,clean,ctx),
            current_consumers=consumers,context_record_ids=[r['id'] for r in roles['source_records']],
            dynamic_startup_fallback_not_actual_scene_assignment=True,
            name_localization_andfresh_display_approval_pending=True))
    save(args.out,dict(records=records,scoped_actors=len(records),runtime=receipt,
        fresh_actor_IDs=fresh,fresh_native_name_getters=2*len(fresh),
        exact_reused_native_name_getters=2*len(old_actors),
        exact_current_snapshot_ARM9_COMMON_andall_source_current_fields_reused=True,
        no_future_roster_orconditional_participation_claim=True,
        current_names_data_not_global_editorial_orfont_approval=True,
        evidence={str(p):digest(p) for p in [args.names,args.roles,Path(__file__)]},new_credit=0))
    print('Reused',2*len(old_actors),'exact getters;bound',2*len(fresh),'fresh getters for',fresh,
        [(r['actor_ID'],[(c['consumer'],c['text']) for c in r['current_consumers']]) for r in records if r['actor_ID'] in fresh])


if __name__=='__main__':
    main()
