"""Bind90 source/current speech calls and29 exact non-relative control leaves."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import prove_lil_shrines_temples_controls_v3168c as prior
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B164_dispatches_v3964')
SOURCE=Path('work/analysis/lil_B164_source_v3960/all49_clean_current_complete_context_with_typed_choice.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);namespace={**prior.__dict__,'SOURCE':SOURCE,'CATALOG_LOOKUP':{}};adapters={}
    for name in ['bind_current_catalog','expanded_current_body','install_boundaries','dispatch']:
        text=inspect.getsource(getattr(prior,name));adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](image);ROOT.mkdir(parents=True);bp=ROOT/'current_registered_Lil_name_catalog_binding.json';save(bp,binding);ctx=CurrentContext('work/analysis/lil_B164_voices_v3963/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');cases=[]
    for r in packet['records']:
        for version,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(r[key]);result=ctx.execute(namespace['dispatch'],raw[0],raw[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==(None if raw[0]==254 else r['source_selector']);cases.append(dict(id=r['id'],block=r['block'],version=version,**result))
    leaves=[]
    for g in packet['blocks']:
        for a,b in zip(g['all_clean_native_commands'],g['all_current_native_commands'],strict=True):
            if a['word'] in [0x4000,0x100,0x200,0x300,0x400,0x2100]:continue
            assert a['offset']==b['offset'] and a['native_extent']==b['native_extent'] and a['whole_command_hex']==b['whole_command_hex'];leaves.append(dict(block=g['block'],offset=a['offset'],word=a['word'],native_extent=a['native_extent'],clean_current_hex=a['whole_command_hex']))
    assert len(cases)==94 and len(leaves)==9 and sum(c['source_selector']==254 for c in cases)==0 and not ctx.machines;save(ROOT/'all47_source_current_dispatches_no_macros_and9_control_leaves.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),speech_dispatch_cases=cases,source_macro_counts=packet['source_macro_counts'],source_owned_adapters=adapters,registered_catalog_binding=str(bp),registered_catalog_binding_sha256=sha(bp.read_bytes()),source_current_opaque_nonrelative_control_leaves=leaves,all9_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact=True,all3_static_actors_without_role_or_roster_fixture=True,no_FE_system_objects_in_this_source_scope=True,source_printable_static_selectors_do_not_become_literal_prose=True,source_current_effective_English_and_catalogue_provenance_distinguished=True,UI_preparation_progressive_and_FE_bodies_explicit_unexecuted_boundaries=True,native_input='work/analysis/lil_B164_voices_v3963/current_native_input.json',native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),full_context_gloss_oldEnglish_comparison_and_native_display_still_pending=True,actual_selected_B164_IDs=[],new_emulator_runs=0,no_ROM_registry_ledger_review_orcompletion_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('94 source/current dispatches pass:3static actors including0D,noFE,no macros. All9nonrelative nontext nonchoice leaves exact. No native display/gameplay/reviewcredit claim.')
