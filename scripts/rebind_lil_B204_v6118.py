"""Rebind unchanged B204 source/current records to registered V6110 and its own snapshot."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6097 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_current_v6118')
OLD=Path('work/analysis/lil_B204_source_v6062/all20_clean_current_complete_context.json')
VERIFIED=Path('work/analysis/editorial_handoff_verification_v6116/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();v,old=map(read,[VERIFIED,OLD]);assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==v['ledger_sha256']
    im=NdsImage.open(v['candidate']);parent=NdsImage.open(old['current_ROM']);clean=NdsImage.open('work/clean.nds');arm=im.read_file('/__arm9__.bin');common=im.read_file('/COMMON/MESFILE.DK4')
    assert sha(Path(v['candidate']).read_bytes())==v['candidate_sha256']
    for i in range(4):assert im.read_file(f'/data/SC{i}.DK4')==parent.read_file(f'/data/SC{i}.DK4')
    assert im.read_file('/data/EV2.DK4')==parent.read_file('/data/EV2.DK4')
    blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks;source=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[204]
    for r in old['records']:
        for b,k,ref in [(source,'source_hex',r['source_reference']),(blocks[204],'current_hex',r['current_reference'])]:
            raw=bytes.fromhex(r[k]);assert b[ref['offset']:ref['offset']+len(raw)]==raw and b[ref['offset']+len(raw)]==0
            assert b[ref['header_offset']:ref['offset']+1].hex()==r['source_complete_preamble_hex']
    inp=deepcopy(read('work/analysis/shachihoko_native_v6098/target_native_input.json'));assert inp['current_ROM_sha256']==v['candidate_sha256'];inp['current_ROM']=v['candidate']
    ROOT.mkdir(parents=True);inputpath=ROOT/'current_native_input.json';save(inputpath,inp);ctx=CurrentContext(inputpath,'unused-no-historical-ROM',ROOT/'current_context')
    assert not ctx.machines
    context=read(inp['native_context_proof']);report=read(context['capture_report']);snap=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==context['frame'])
    new=deepcopy(old);keys=['current_ROM','current_ROM_sha256','current_ARM9_sha256','current_COMMON_sha256','actual_historical_snapshot','actual_historical_snapshot_sha256','historical_snapshot_ROM','current_actual_context_capture_report','current_actual_context_report_sha256','current_actual_context_snapshot']
    new['historical_pre_V6110_context_metadata']={k:deepcopy(old[k]) for k in keys}
    new.update(current_ROM=v['candidate'],current_ROM_sha256=v['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),actual_historical_snapshot=snap['path'],actual_historical_snapshot_sha256=snap['sha256'],historical_snapshot_ROM=v['candidate'],current_actual_context_capture_report=context['capture_report'],current_actual_context_report_sha256=context['capture_report_sha256'],current_actual_context_snapshot=deepcopy(snap),context_is_current_Lil_opening_not_B204_activation=True,predecessor_source_packet=str(OLD),predecessor_source_packet_sha256=sha(OLD.read_bytes()),all_source_current_story_EV2_record_preambles_and_control_inputs_exact_to_predecessor=True,current_strict_native_input=str(inputpath),current_strict_native_input_sha256=sha(inputpath.read_bytes()),current_strict_context_plan=str(ctx.proof_path),current_strict_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False)
    save(ROOT/'all20_clean_current_complete_context.json',new)
    save(ROOT/'rebind_receipt.json',dict(candidate=v['candidate'],candidate_sha256=v['candidate_sha256'],source_packet=str(OLD),source_packet_sha256=sha(OLD.read_bytes()),current_packet=str(ROOT/'all20_clean_current_complete_context.json'),current_packet_sha256=sha((ROOT/'all20_clean_current_complete_context.json').read_bytes()),all_four_story_files_EV2_and20_source_current_text_preambles_exact=True,own_actual_snapshot_bound_to_identical_registered_whole_ROM=True,strict_current123264_pool_and_executed_instruction_guards_preserved=True,no_historical_RAM_overlay_or_new_emulator_run=True,new_review_credit=0,full_goal_complete=False))
    print('B20420 exact source/current records rebound to registered V6110 and its own actual snapshot;no new boot or credit.')
