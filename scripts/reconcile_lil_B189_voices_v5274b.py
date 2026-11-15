"""Rebind all207 current names/eight voice classes and the four B189 actors from actual V5263 RAM."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B189_voices_v5274b')
SOURCE=Path('work/analysis/lil_B189_source_v5273b/all17_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);assert source['source_static_actor_selectors']==[82,104,113,147]
    conf=read('translations/shop657_full_width_reflow_release_v1.json');ROOT.mkdir(parents=True);context=ROOT/'current_capture_context.json'
    save(context,dict(capture_report=source['current_actual_context_capture_report'],capture_report_sha256=source['current_actual_context_report_sha256'],frame=4000,snapshot_sha256=source['current_actual_context_snapshot']['sha256'],directory_sha256=conf['directory_sha256']))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=source['current_COMMON_sha256'],native_context_proof=str(context)))
    ctx=CurrentContext(inp,source['historical_snapshot_ROM'],ROOT/'current_context');catalog=ctx.execute(names);ctx.machines.pop();resolution=ctx.execute(selectors,source['source_static_actor_selectors']);ctx.machines.pop()
    assert len(catalog['rows'])==207 and {r['original_voice_class'] for r in catalog['rows']}==set(range(8)) and not ctx.machines
    fresh={r['actor_ID']:r for r in catalog['rows'] if r['actor_ID'] in [82,104,113,147]};assert len(fresh)==4
    save(ROOT/'current207_catalog_eight_voices_and_four_source_selectors.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),catalog=catalog,fresh4_actor_names=dict(rows=list(fresh.values())),original_static_selector_resolution=resolution,all207_names_and_eight_voice_classes_freshly_executed_on_current_snapshot=True,context_is_current_Lil_opening_not_B189_activation=True,progressive_nameplate_and_full_catalogue_distinction_pending=True,no_rank_kinship_profession_or_relationship_inferred_from_collecting_or_sales_register=True,FE_not_passed_to_static_actor_getters=True,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print({i:dict(name=r['current_catalog_name'],voice=r['original_voice_class']) for i,r in fresh.items()})
