"""Seal both menu labels and all speech references with a source-locked inverse helper."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.rafael_B46_profile_v1 import validate_approved_batch
from dk4tool.dialogue.rafael_B46_choices_v1 import compile_choices
from scripts.source_locked_derivation_v5118 import derive
from scripts.Rafael_B46_release_paths_v7958 import PARENT,ROM,DRAFT,APPROVED,MENU,MAP,SEAL,RELOCATION,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_reference_tools_v7958')
HELPER=Path('dk4tool/patch/rafael_B46_reconstruction_v1.py')
MENU_PATCH='''
    require(len(group['choice_commands'])==1 and len(choice_rows)==2,'one complete two-choice menu')
    choice=group['choice_commands'][0];at=choice['old_offset'];before=bytes.fromhex(choice['old_hex']);ja=bytes.fromhex(choice['clean_hex'])
    require(at==256 and len(before)==len(ja)==choice['old_length']==36 and choice['count']==2 and choice['word']==0x2100,'source menu extent/count')
    require(old[at:at+36]==before and clean[at:at+36]==ja,'literal source/current complete menu')
    require(typed.hex()==choice['target_hex'] and len(typed)==choice['new_length']==30,'compiled complete menu')
    require(choice['record_IDs']==[r['id'] for r in choice_rows] and choice['labels']==[r['english'] for r in choice_rows],'original choice order')
    for index,(row,ref) in enumerate(zip(choice_rows,choice['label_references'],strict=True)):
        require(row['option_index']==ref['option_index']==index and row['command_offset']==at and row['block']==group['block'] and row['file_path']==group['file_path'],'choice scope/index')
        require(row['id']==ref['id'] and row['source_reference']==ref['source_reference'] and row['current_reference']==ref['old_reference'],'source/current choice references')
        for data,key,reference in [(old,'current_hex',row['current_reference']),(clean,'source_hex',row['source_reference'])]:
            offset=reference['offset'];raw=bytes.fromhex(row[key])
            require(data[offset:offset+len(raw)+1]==raw+b'\\0' and data[:offset].count(b'\\0')==reference['record_index'],'literal choice record')
        require(row['english'].encode('ascii').hex()==ref['target_hex']==row['compiled_hex'] and len(row['english'])==ref['new_length'],'choice bytes')
    patches.append(dict(start=at,end=at+36,old=before,source=ja,value=typed,id='complete-native-menu'))
'''
MENU_REFS='''
    require(mapped(choice['old_offset'])==choice['new_offset']==242,'relocated complete menu offset')
    for ref in choice['label_references']:
        field=choice['new_offset']+2+2*ref['option_index'];base=choice['new_offset']+6;relative=struct.unpack_from('<H',target,field)[0]
        at=base+relative
        require(field==ref['relative_table_field'] and base==ref['relative_base'] and relative==ref['relative_offset'],'native menu internal table')
        require(at==ref['new_offset'] and target[at:at+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\\0' and target[:at].count(b'\\0')==ref['new_record_index'],'final choice reference')
'''
def summary(group):
    return dict(choice=group['choice'],source_English_exits=group['source_English_exits'],
        command_difference_rows=len(group['command_comparison_differences']),duration_difference_rows=len(group['duration_differences']),
        later_RGB_differences=len(group['later_RGB_differences']),later_samples=group['later_sample_count'],
        five_component_equality=group['five_native_component_equality'],whole_actor_equality=group['whole_actors_equal'],
        final_PRNG_seeds=group['final_PRNG_seeds'],raw_calendars_no_invented_date_interpretation=group['raw_calendars_no_invented_date_interpretation'])
if __name__=='__main__':
    assert not ROOT.exists() and all(not p.exists() for p in [APPROVED,MENU,MAP,SEAL,HELPER])
    result=derive('dk4tool/patch/rafael_B45_reconstruction_v1.py',str(HELPER),{
        'B45':'B46',
        'def reconstruct(old,clean,group,packet,rows,edges):':'def reconstruct(old,clean,group,packet,rows,edges,choice_rows,typed):',
        "    patches.sort(key=lambda p:p['start']);":MENU_PATCH+"\n    patches.sort(key=lambda p:p['start']);",
        "        else:require(previous['whole_command_hex']==new['whole_command_hex'],'opaque control/resource/effect/wait/end')":
            "        elif word==0x2100:require(a==choice['old_offset'] and z==choice['new_offset'] and target[z:z+new['native_extent']]==typed,'complete original-provider menu')\n        else:require(previous['whole_command_hex']==new['whole_command_hex'],'opaque control/resource/effect/wait/end')",
        '    for clean_version in [False,True]:':MENU_REFS+'\n    for clean_version in [False,True]:',
    })
    from dk4tool.patch.rafael_B46_reconstruction_v1 import reconstruct
    doc=read(DRAFT);validate_approved_batch(doc);typed=compile_choices(doc['typed_choice_records'])
    mapping=read(RELOCATION);p=proofs();data={k:read(path) for k,path in p.items()}
    current,policy,approval,actual,later,branches=[data[k] for k in ['source_context','native_policy_validation','actual_approval','actual_proof','later_scope_proof','source_branch_proof']]
    assert approval['manuscript_sha256']==sha(DRAFT.read_bytes()) and policy['positive_speeches']==24 and policy['negative_count']==300
    assert not actual['unresolved'] and len(actual['groups'])==4
    assert sha(PARENT.read_bytes())==mapping['candidate_sha256']==current['current_ROM_sha256']
    parent,reference,clean=[NdsImage.open(path) for path in [PARENT,ROM,'work/clean.nds']]
    oldbank,newbank,cleanbank=[IlnkContainer.parse(im.read_file('/data/SC0.DK4')).blocks for im in [parent,reference,clean]]
    group=deepcopy(mapping['groups'][0]);assert group['block']==46
    target=reconstruct(oldbank[46],cleanbank[46],group,current['groups'][0],doc['records'],branches['operands_requiring_adjustment_when_resizing'],doc['typed_choice_records'],typed)
    assert target==newbank[46] and len(target)==1528
    assert [i for i,(a,b) in enumerate(zip(oldbank,newbank,strict=True)) if a!=b]==[46] and len(oldbank)==343
    restored=list(newbank);restored[46]=oldbank[46]
    assert IlnkContainer(restored).to_bytes()==parent.read_file('/data/SC0.DK4')
    assert [path for _,path,v in parent.iter_files() if reference.read_file(path)!=v]==['/data/SC0.DK4']
    assert all(reference.read_file(path)==v for path,v in parent.iter_components())
    assert data['native_caller_proof']['all_command_maps']==group['command_map'] and data['native_caller_proof']['relative_operand_maps']==group['relative_fixups']
    group.update(route=0,route_identity='Rafael',external_references_complete=True,original_entry_payload_offset=8,
        source_archive_sha256=sha(parent.read_file('/data/SC0.DK4')),target_archive_sha256=sha(reference.read_file('/data/SC0.DK4')),
        approved_manuscript=str(DRAFT),approved_manuscript_sha256=sha(DRAFT.read_bytes()))
    evidence={str(path):sha(path.read_bytes()) for path in [DRAFT,RELOCATION,*map(Path,p.values()),HELPER,Path(__file__),Path('scripts/Rafael_B46_release_paths_v7958.py')]}
    save(MAP,dict(format='dk4-Rafael26-B46-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),file_path='/data/SC0.DK4',
        source_archive_sha256=group['source_archive_sha256'],target_archive_sha256=group['target_archive_sha256'],
        groups=[group],preserve_record_parity=True,observed_comparison_contract=[summary(g) for g in later['groups']],
        evidence=evidence,**{k:True for k in FLAGS},new_credit=0,full_goal_complete=False))
    successor=deepcopy(doc)
    for row in successor['records']:
        positive=next(r for r in policy['positive_cases'] if r['id']==row['id'])
        ref=next(r for r in group['text_records'] if r['id']==row['id'])
        row.update(base_QA_report=positive['qa'],qa_waivers=[],qa_waiver_reason=None,native_page_count=1,
            target_reference=dict(block=46,offset=ref['new_offset'],bytes=ref['new_length'],header_offset=ref['new_offset']-5,record_index=ref['new_record_index']),
            stored_target_hex=ref['target_hex'],stored_parity_space=ref['parity_space_added'])
    for row,ref in zip(successor['typed_choice_records'],group['choice_commands'][0]['label_references'],strict=True):
        assert row['id']==ref['id']
        row.update(target_reference=dict(block=46,command_offset=242,offset=ref['new_offset'],bytes=ref['new_length'],
            relative_table_field=ref['relative_table_field'],relative_base=ref['relative_base'],relative_offset=ref['relative_offset'],record_index=ref['new_record_index']))
    successor.update(native_approved_manuscript=str(DRAFT),native_approved_manuscript_sha256=sha(DRAFT.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),
        reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),
        status='26 exact decisions sealed;atomic registered integration pending')
    validate_approved_batch(successor)
    menu={k:deepcopy(v) for k,v in successor.items() if k not in ['records','typed_choice_records']}
    menu.update(encoder='typed-menu-relocatable-v1',records=deepcopy(successor['typed_choice_records']),total_editorial_objects=2,
        revisions=0,retentions=2,mixed_speech_manuscript=str(APPROVED),native_approved_manuscript=str(DRAFT),
        status='two native menu labels sealed;atomic registered integration pending')
    save(APPROVED,successor);save(MENU,menu);SEAL.parent.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),
        choice_manuscript=str(MENU),choice_manuscript_sha256=sha(MENU.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),all26_five_gates_andexact_references_approved=True,
        all37_commands4_relative_sites20_cases_source_bound=True,complete_clean_predecessor_blocks_andwhole_archive_inverse_exact=True,
        actual24_each_language_both_choices_andall_measured_limits_preserved=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True)
    save(ROOT/'provenance.json',dict(reconstruction_derivation=result,source00_body_guard_andall_original_native_integer_constants_preserved=True,
        approved=str(APPROVED),approved_sha256=sha(APPROVED.read_bytes()),choice_manuscript=str(MENU),choice_manuscript_sha256=sha(MENU.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),no_ROM_registration_orcompletion_credit=True,full_goal_complete=False))
    print('26 B46 decisions sealed;24 speeches,one native two-choice object,all37commands/four relatives andboth full inverses. Atomic production pending;zero credit.')
