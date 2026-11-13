"""Fresh207 catalogue/eight voices and three source selectors on current V4821 RAM."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B181_voices_v4833')
SOURCE=Path('work/analysis/lil_B181_source_v4832/all10_clean_current_complete_context.json')

if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE)
    conf=read('translations/shop657_full_width_reflow_release_v1.json')
    ROOT.mkdir(parents=True);context=ROOT/'current_capture_context.json'
    save(context,dict(capture_report=source['current_actual_context_capture_report'],
        capture_report_sha256=source['current_actual_context_report_sha256'],frame=4000,
        snapshot_sha256=source['current_actual_context_snapshot']['sha256'],directory_sha256=conf['directory_sha256']))
    inp=ROOT/'current_native_input.json'
    save(inp,dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=source['current_COMMON_sha256'],native_context_proof=str(context)))
    ctx=CurrentContext(inp,source['historical_snapshot_ROM'],ROOT/'current_context')
    catalog=ctx.execute(names);ctx.machines.pop()
    resolution=ctx.execute(selectors,source['source_static_actor_selectors']);ctx.machines.pop();assert not ctx.machines
    assert len(catalog['rows'])==207 and {r['original_voice_class'] for r in catalog['rows']}==set(range(8))
    old=read('work/analysis/lil_B180_voices_v4775/current207_catalog_eight_voices_and_two_source_selectors.json')
    fresh={r['actor_ID']:r for r in catalog['rows'] if r['actor_ID'] in [166,167,168]}
    for r in old['catalog']['rows']:
        if r['actor_ID'] not in fresh:continue
        for key in ['actor_ID','getter','current_catalog_name','original_voice_class']:
            assert fresh[r['actor_ID']][key]==r[key]
    assert {i:r['current_catalog_name'] for i,r in fresh.items()}=={166:'Lady',167:'Lady',168:'Lady'}
    assert all(r['original_voice_class']==0 for r in fresh.values())
    save(ROOT/'current207_catalog_eight_voices_and_three_source_selectors.json',dict(candidate=source['current_ROM'],
        candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        catalog=catalog,fresh3_actor_names=dict(rows=list(fresh.values())),original_static_selector_resolution=resolution,
        all207_names_and_eight_voice_classes_freshly_executed_on_current_snapshot=True,
        prior_three_source_names_voices_getters_semantically_equal_without_assuming_object_addresses=True,
        context_is_current_Lil_opening_not_B181_activation=True,FE_not_passed_to_static_actor_getters=True,
        current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),current_native_context_plan=str(ctx.proof_path),
        current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,no_ROM_registry_orledger_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Fresh207 current names/eight voices and Lady166/Lady167/Lady168 selectors pass;current opening context,no B181 gameplay or credit.')
