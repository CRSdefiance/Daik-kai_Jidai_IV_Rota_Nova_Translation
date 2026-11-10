"""Reuse scoped name bindings and execute only missing native role-fallback getters."""
import argparse
import inspect
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.write_rafael_B169_contextual_v1 import fields,getter


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['names','roles','out']:p.add_argument('--'+name,type=Path,required=True)
    args=p.parse_args();assert not args.out.exists()
    names,roles=map(load,[args.names,args.roles]);runtime=names['runtime'];assert runtime==roles['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=runtime['captain']);assert ctx.receipt()==runtime
    known={r['actor_ID'] for r in names['records']}
    missing=sorted({r['resolved_actor_ID'] for r in roles['native_roles']['rows']}-known)
    assert missing and all(0<=actor<207 for actor in missing)
    source=checked_text(inspect.getsource(getter),{'for ident in [2,4,13,23,109]:':'for ident in ACTORS:'})
    env={**getter.__globals__,'ACTORS':missing}
    exec(compile(source,__file__+'::same-both-original-scoped-native-name-getters','exec'),env)
    fresh=ctx.execute(env['names']);assert len(fresh['rows'])==2*len(missing)
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    result=deepcopy(names)
    for actor in missing:
        selectors={r['source_selector'] for r in roles['native_roles']['rows'] if r['resolved_actor_ID']==actor}
        consumers=[r for r in fresh['rows'] if r['actor_ID']==actor]
        assert {r['consumer'] for r in consumers}=={'progressive-nameplate','full-catalogue'}
        result['records'].append(dict(actor_ID=actor,source_andcurrent_fields=fields(actor,clean,ctx),current_consumers=consumers,
            context_record_ids=[r['id'] for r in roles['source_records'] if r['source_selector'] in selectors],
            spoken_reference_only=False,current_startup_role_fallback_only=True,future_conditional_participation_unvisited=True,
            name_localization_andfresh_display_approval_pending=True))
    result['records'].sort(key=lambda r:r['actor_ID'])
    assert all(next(r for r in result['records'] if r['actor_ID']==old['actor_ID'])==old for old in names['records'])
    result.update(scoped_actors=len(result['records']),original_native_name_getters=2*len(result['records']),
        exact_existing_scoped_getters_reused=names['original_native_name_getters'],fresh_role_name_getters=len(fresh['rows']),
        original_name_binding=str(args.names),original_name_binding_sha256=digest(args.names),
        role_binding=str(args.roles),role_binding_sha256=digest(args.roles),role_getter_execution=fresh,
        default_macro_cases_reused_without_reexecution=True,new_credit=0)
    result.setdefault('evidence',{}).update({str(p):digest(p) for p in [args.names,args.roles,Path(__file__)]})
    save(args.out,result);print('Added',missing,'using',len(fresh['rows']),'fresh getters; reused',names['original_native_name_getters'],'exact scoped getters.')


if __name__=='__main__':main()
