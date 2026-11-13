"""Seal exact clean/current/stored/relocated references after original loader and control checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.maria_B97_reference_paths_v5021 import PARENT,ROM,PLAN,STORED,DOC
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_reference_approval_v5026')
OUTPUT=Path('translations/maria_B97_editorial_manuscript_v6.json')
MAP=Path('translations/maria_B97_editorial_relocation_map_v1.json')
LOADER=Path('work/analysis/maria_B97_loader_v5022/whole_SC3_and_B97_initial_entry_proof.json')
CENSUS=Path('work/analysis/maria_B97_references_v5023/three_entry_censuses_and40_clean_current_target_commands.json')
ENDS=Path('work/analysis/maria_B97_ends_v5024/two_guarded_tail_end_decodes_no_padding_dependency.json')
CONTROLS=Path('work/analysis/maria_B97_relocated_controls_v5025c/all32_final_dispatches_FO_and_eight_relocated_leaves.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not MAP.exists();doc=deepcopy(read(DOC));plan,stored,loader,census,ends,controls=map(read,[PLAN,STORED,LOADER,CENSUS,ENDS,CONTROLS])
    assert stored['stored_alignment_cases']==128 and stored['fresh_parity_alignment_cases']==72 and stored['exact_byte_reused_alignment_cases']==56
    assert loader['all303_whole_blocks_and606_modes_each_pass'] and census['all40_complete_preambles_and8_exact_leaves_preserved'] and ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read'] and len(controls['relocated_dispatch_cases'])==32 and len(controls['all8_source_current_target_exact_leaves'])==8
    images=[NdsImage.open(p) for p in [PARENT,ROM,'work/clean.nds','out/raphael_natural_v2_accepted_base.nds']];blocks=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[97] for im in images]
    a,b,jp=blocks[:3];assert (len(a),len(b))==(1904,2048) and b[:4]==a[:4]==jp[:4]==b'CS\1\1'
    rows={r['id']:r for r in doc['records']};texts=[]
    for t in plan['text_records']:
        r=rows[t['id']];oldat,newat=r['current_reference']['offset'],t['new_text_offset'];old=bytes.fromhex(r['current_hex']);value=bytes.fromhex(t['stored_text_hex']);j=bytes.fromhex(r['source_hex']);sa=r['source_reference']['offset']
        assert a[oldat:oldat+len(old)+1]==old+b'\0' and b[newat:newat+len(value)+1]==value+b'\0' and jp[sa:sa+len(j)+1]==j+b'\0'
        assert a[oldat-5:oldat+1]==b[newat-5:newat+1]==jp[sa-5:sa+1]==bytes.fromhex(r['source_complete_preamble_hex'])
        ref=dict(t,old_offset=oldat,old_length=len(old),new_offset=newat,new_length=len(value),record_index=r['current_record_index'],new_record_index=b[:newat].count(b'\0'))
        assert a[:oldat].count(b'\0')==ref['record_index']==ref['new_record_index'];texts.append(ref)
        r.update(reference_target=dict(block=97,offset=newat,header_offset=t['new_command_offset'],bytes=len(value),record_index=ref['new_record_index']),reference_target_hex=value.hex(),native_display_consumer='original_null_actor_FE_24310_then5473C' if r['kind']=='system-FE' else 'original_progressive_54020',actual_B33_content_fixture_observed=True,status='all-editorial-native-reference-and-focused-actual-gates-approved;registered-release-startup-pending')
    evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,STORED,LOADER,CENSUS,ENDS,CONTROLS,Path(doc['actual_proof']),Path(__file__)]}
    mapping=dict(format='dk4-maria-B97-source-relocation-map-v1',file_path='/data/SC3.DK4',block=97,required_runtime_ARM9_sha256=sha(images[0].read_file('/__arm9__.bin')),source_SC3_sha256=sha(images[0].read_file('/data/SC3.DK4')),target_SC3_sha256=sha(images[1].read_file('/data/SC3.DK4')),clean_SC3_sha256=sha(images[2].read_file('/data/SC3.DK4')),canonical_SC3_sha256=sha(images[3].read_file('/data/SC3.DK4')),source_block_sha256=sha(a),target_block_sha256=sha(b),clean_block_sha256=sha(jp),entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,text_records=texts,mapped_native_commands=plan['mapped_native_commands'],relative_skip_fixups=[],source_plan=str(PLAN),source_census=str(CENSUS),target_block=plan['target_block'],source_logical_end=1902,target_logical_end=2046,source_stored_bytes=1904,target_stored_bytes=2048,all40_source_commands32_complete_preambles8_exact_leaves_verified=True,all32_final_stored_targets128_macro_cases_and_native_planes_verified=True,one_source_FO31_progressive_one_FE_and_source72_two_pages_preserved=True,all302_other_SC3_blocks_every_other_file_component_and_original_B33_exact=True,exact_inverse_recovers_all_predecessor_bytes_including_tail=True,source_EV3_event97_action98_and_original_block_index_loader_bound=True,focused_actual_B97_content_in_B33_fixture_approved=True,source_event97_natural_eligibility_and_earned_inventory_not_claimed=True,no_open_translation_specific_display_or_control_finding=True,final_RGB_actor_and_PRNG_inequality_disclosed=True,loader_proof=str(LOADER),stored_target_proof=str(STORED),relocated_control_proof=str(CONTROLS),termination_decode_proof=str(ENDS),actual_display_proof=doc['actual_proof'],evidence=evidence,full_goal_complete=False)
    save(MAP,mapping)
    doc.update(previous_manuscript=str(DOC),previous_manuscript_sha256=sha(DOC.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_map_pending=False,status='all-editorial-native-reference-and-focused-actual-gates-approved;registered-release-startup-pending',registered_integration_pending=True,source_prose_or_completion_credit_added=0)
    for key,path in [('final_padding_proof',STORED),('loader_proof',LOADER),('reference_census_proof',CENSUS),('termination_decode_proof',ENDS),('relocated_control_proof',CONTROLS),('source_nameplate_consumer_proof',Path(doc['name_consumer_proof'])),('representative_proof',Path(doc['actual_proof'])),('native_review_proof',Path(doc['native_review_proof']))]:doc[key]=str(path);doc[key+'_sha256']=sha(path.read_bytes())
    validate_natural_dialogue_batch(doc);save(OUTPUT,doc);ROOT.mkdir(parents=True)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(OUTPUT),manuscript_sha256=sha(OUTPUT.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),all32_source_native_reference_and_focused_actual_gates_approved=True,all32_prose_and_compiled_targets_unchanged=True,all40_commands_and8_leaves_preserved=True,source72_two_pages_original_guard_indent6_and_A_advance_preserved=True,source_unearned_fixture_and_postscene_state_differences_disclosed=True,registered_release_startup_and_credit_pending=True,evidence=evidence,new_review_credit=0,new_emulator_runs=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('All32 exact source/native/reference/focused-actual objects sealed;registered cumulative release/startup pending.')
