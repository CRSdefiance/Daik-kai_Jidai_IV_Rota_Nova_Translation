"""Execute all target description/name getters on its own actual expanded-payload snapshot."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6097 import CurrentContext
from scripts.bind_shachihoko_description_consumers_v6092b import collect
from scripts.prove_shachihoko_item_consumers_v6081b import consumers
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_native_v6098')
RECEIPT=Path('work/analysis/shachihoko_item116_research_v6094/coordinated_research_receipt.json')
BIND=Path('work/analysis/shachihoko_description_consumers_v6092/current218_live_description_getters_two_item_callers_and_exact_owned_representations.json')
if __name__=='__main__':
    assert not ROOT.exists();receipt,binding=map(read,[RECEIPT,BIND]);plan=receipt['data_plan'];terminal_path=Path('work/analysis/shachihoko_runs_v6095/newgame_terminal.json');terminal=read(terminal_path);assert terminal['terminal']
    report_path=Path(terminal['report']);report=read(report_path);assert sha(report_path.read_bytes())==terminal['report_sha256'] and report['ROM_sha256']==receipt['research_ROM_sha256']==sha(Path(receipt['research_ROM']).read_bytes())
    snapshot=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==4000);assert snapshot['read_only_export'] and sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
    ROOT.mkdir(parents=True);context=ROOT/'target_capture_context.json';save(context,dict(capture_report=str(report_path),capture_report_sha256=sha(report_path.read_bytes()),frame=4000,snapshot_sha256=snapshot['sha256'],directory_sha256=plan['new_directory_sha256']))
    inp=ROOT/'target_native_input.json';save(inp,dict(current_ROM=receipt['research_ROM'],current_ROM_sha256=receipt['research_ROM_sha256'],current_ARM9_sha256=plan['target_ARM9_sha256'],current_COMMON_sha256=plan['target_COMMON_sha256'],native_context_proof=str(context)))
    ctx=CurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');description=ctx.execute(collect,binding['advice_helper']);ctx.machines.pop();names=ctx.execute(consumers);ctx.machines.pop();assert not ctx.machines
    differences=[]
    for old,new in zip(binding['native']['cases'],description['cases'],strict=True):
        assert all(old[k]==new[k] for k in ['item_ID','message_ID'])
        if old!=new:
            assert old['item_ID']==116 and old['pointer']==plan['old_compiled_pointer'] and new['pointer']==plan['new_compiled_pointer'] and new['paragraph']==plan['description']
            assert new['terminated_rows_hex']==[v.encode().hex() for v in plan['compiled_rows']];differences.append(dict(before=old,after=new))
    assert len(differences)==1
    earlier=read('work/analysis/shachihoko_item_consumers_v6081b/all218_item_getters_two_original_callers_and_complete_native_title_plane.json')['versions'][1]['result']['rows']
    assert names['rows']==earlier
    save(ROOT/'all218_live_descriptions_and218_item_names_rebound_to_actual_target.json',dict(
        candidate=receipt['research_ROM'],candidate_sha256=receipt['research_ROM_sha256'],ARM9_sha256=plan['target_ARM9_sha256'],COMMON_sha256=plan['target_COMMON_sha256'],
        all218_native_COMMON_then_private_description_lookups=description,only_item116_description_changes=differences,
        all218_original_virtual_static_item_names_and436_callers=names,
        all217_other_compiled_paragraphs_pointers_and_all218_previous_target_name_outputs_exact=True,
        all_actual123264_deployed_payload_bytes_and_executed_target_instructions_exact=True,
        no_historical_initialized_RAM_overlay_or_synthetic_item_ownership=True,
        target_native_input=str(inp),target_native_input_sha256=sha(inp.read_bytes()),target_context_plan=str(ctx.proof_path),target_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        native_item_detail_fonts_parent_crops_actual_description_and_registered_release_pending=True,
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RECEIPT,BIND,terminal_path,report_path,Path(__file__),Path('scripts/current_build_native_context_v6097.py')]}))
    print('Actual target snapshot:218 description lookups and218 virtual/static names/436 callers pass. Only description116 changes;all217 other paragraphs and prior target names exact.')
