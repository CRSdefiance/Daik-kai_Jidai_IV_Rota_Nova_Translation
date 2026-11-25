"""Rebind current actor identities/voice classes without mistaking technical coverage for editorial review."""
from pathlib import Path
from scripts.current_build_native_context_v6097 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B205_voices_v6173');SOURCE=Path('work/analysis/lil_B205_source_v6172/all17_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);assert source['source_static_actor_selectors']==[2,15]
    inp=Path('work/analysis/current_V6160_native_v6168/current_native_input.json');assert read(inp)['current_ROM_sha256']==source['current_ROM_sha256']
    ROOT.mkdir(parents=True);ctx=CurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');catalog=ctx.execute(names);ctx.machines.pop();resolution=ctx.execute(selectors,[2,15]);ctx.machines.pop()
    assert len(catalog['rows'])==207 and {r['original_voice_class'] for r in catalog['rows']}==set(range(8)) and not ctx.machines
    rows=[r for r in catalog['rows'] if r['actor_ID'] in [2,15]];assert len(rows)==2
    save(ROOT/'current207_catalog_eight_voices_and_two_source_selectors.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),catalog=catalog,fresh2_actor_names=dict(rows=rows),original_static_selector_resolution=resolution,all207_names_and_eight_voice_classes_freshly_executed_on_current_snapshot=True,context_is_current_Lil_opening_not_B205_activation=True,progressive_nameplate_and_full_catalogue_distinction_pending=True,FE_not_passed_to_static_actor_getters=True,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),no_new_name_dialogue_editorial_completion_credit=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Current207 names/eight voice classes and two B205 static selectors bound. No source scene or editorial-name approval inferred.')
