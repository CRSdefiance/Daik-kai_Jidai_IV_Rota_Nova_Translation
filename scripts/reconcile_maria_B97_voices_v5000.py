"""Fresh207 names/eight voices and three static selectors in current captain3 context."""
from pathlib import Path
import inspect
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names
from scripts.reconcile_maria_B109_voices_v3499 import resolve
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/maria_B97_voices_v5000')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);ROOT.mkdir(parents=True)
    context=ROOT/'current_capture_context.json';directory=read('translations/shop657_full_width_reflow_release_v1.json')['directory_sha256']
    save(context,dict(capture_report=source['current_actual_context_capture_report'],capture_report_sha256=source['current_actual_context_report_sha256'],
        frame=31000,snapshot_sha256=source['current_actual_context_snapshot']['sha256'],directory_sha256=directory,
        existing_system_unlock_manifest=source['existing_system_unlock_manifest'],existing_system_unlock_manifest_sha256=source['existing_system_unlock_manifest_sha256']))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=source['current_COMMON_sha256'],native_context_proof=str(context)))
    ctx=CurrentContext(inp,source['historical_snapshot_ROM'],ROOT/'current_context')
    text=inspect.getsource(names)
    for old,new in [('assert get(0x7F244)==2','assert get(0x7F244)==3'),('if ident==2 else','if ident==3 else')]:assert text.count(old)==1;text=text.replace(old,new)
    env=dict(names.__globals__);exec(compile(text,str(Path(__file__))+'::current_Maria_names','exec'),env)
    catalog=ctx.execute(env['names']);ctx.machines.pop();resolution=ctx.execute(resolve,source['source_static_actor_selectors']);ctx.machines.pop();assert not ctx.machines
    assert len(catalog['rows'])==207 and {r['original_voice_class'] for r in catalog['rows']}==set(range(8))
    by={r['actor_ID']:r for r in catalog['rows']};assert by[3]['current_catalog_name']=='Maria Huamei Li'
    selected={str(i):by[i] for i in source['source_static_actor_selectors']}
    save(ROOT/'current207_catalog_eight_voices_and_three_Maria_selectors.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),catalog=catalog,fresh_three_actor_names=selected,
        original_static_selector_resolution=resolution,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),
        current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_name_getter_adapter=text,
        all207_names_and_eight_voices_freshly_executed_on_exact_current_Maria_snapshot=True,all_actor_models_and_unowned4MiB_exact=True,
        existing_system_unlock_only_no_actor_role_roster_RNG_or_outcome_fixture=True,
        progressive_nameplates_and_macro_ownership_still_require_binding=True,FE_not_passed_to_static_actor_name_getters=True,
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print({i:(r['current_catalog_name'],r['original_voice_class']) for i,r in selected.items()})
