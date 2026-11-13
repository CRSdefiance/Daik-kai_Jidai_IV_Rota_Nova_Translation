"""Add only the original current fallback's two name consumers; reuse the23 exact bindings."""
from copy import deepcopy
from pathlib import Path
import inspect
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B169_contextual_v1 import fields,getter
from scripts.source_locked_derivation_v5118 import checked_text

ROOT=Path('work/Maria_B196_B215_clean_20261110')


def main():
    prior_path=ROOT/'scoped_names_macros_reference_v1.json';role_path=ROOT/'dynamic_roles_current_v1.json'
    out=ROOT/'scoped_names_macros_reference_v2.json';assert not out.exists()
    prior,roles=map(load,[prior_path,role_path]);assert prior['runtime']==roles['runtime']
    role=next(r for r in roles['native_roles']['rows'] if r['source_selector']==208)
    assert (role['strict_assignment'],role['resolved_actor_ID'],role['source_voice_class'])==(208,156,4)
    assert len(prior['records'])==23 and 156 not in {r['actor_ID'] for r in prior['records']}
    runtime=prior['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3)
    assert ctx.receipt()==runtime
    source=checked_text(inspect.getsource(getter),{'for ident in [2,4,13,23,109]:':'for ident in [156]:'})
    env=dict(getter.__globals__);exec(compile(source,__file__+'::same-two-original-fallback-name-consumers','exec'),env)
    result=ctx.execute(env['names']);assert len(result['rows'])==2
    assert {r['consumer']:r['text'] for r in result['rows']}=={'progressive-nameplate':'Sailor','full-catalogue':'Retainer'}
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    record=dict(actor_ID=156,source_andcurrent_fields=fields(156,clean,ctx),current_consumers=result['rows'],
        context_record_ids=[r['id'] for r in roles['source_records']],spoken_reference_only=False,
        current_startup_fallback_not_future_conditional_assignment=True,name_localization_andfresh_display_approval_pending=True)
    projected=deepcopy(prior);projected['records'].append(record);projected['records'].sort(key=lambda r:r['actor_ID'])
    projected.update(scoped_actors=24,original_native_name_getters=48,
        exact_prior_native_getters_reused=46,fresh_supplementary_native_getters=2,
        original_reference=str(prior_path),original_reference_sha256=digest(prior_path),
        source_role_reference=str(role_path),source_role_reference_sha256=digest(role_path),
        current_fallback_names_not_new_actual_scene_participation=True,
        evidence={**prior['evidence'],**{str(p):digest(p) for p in [prior_path,role_path,Path(__file__)]}})
    save(out,projected)
    print('Bound fallback156 Sailor/Retainer with2 fresh getters; reused46 exact prior getters;24 scoped actors,zero credit.')


if __name__=='__main__':main()
