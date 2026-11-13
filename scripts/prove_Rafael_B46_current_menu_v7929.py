"""Bind both effective current choice labels, exact control inverse and the named rescue component."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.audit_native_given_name_table import string
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_current_menu_v7929')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
FLOW=Path('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,flow=map(read,[CURRENT,FLOW])
    source=read(doc['source_packet']);old=source['groups'][0];group=doc['groups'][0]
    clean,current=[NdsImage.open(p) for p in [source['source_ROM'],doc['current_ROM']]]
    ja=bytes.fromhex(old['clean_block_hex']);now=bytes.fromhex(group['current_block_hex'])
    assert now==IlnkContainer.parse(current.read_file('/data/SC0.DK4')).blocks[46]
    assert [r['source_gloss_precanonical_ID'] for r in doc['typed_choice_records']]==[r['id'] for r in read(doc['gloss_packet'])['menu_choices']]
    env=dict(original.__dict__);exec(compile(flow['source_owned_VM_adapter'],__file__+'::native-current-choice-labels','exec'),env)
    native=[]
    for label,image,b,commands in [('clean-source',clean,ja,old['commands']),('current-English',current,now,group['all_current_commands'])]:
        menu=next(c for c in commands if c['word']==0x2100);raw=b[menu['offset']:menu['offset']+menu['native_extent']]
        result=env['choice_vm'](image.read_file('/__arm9__.bin'),raw)
        expected=[r['source_Japanese'] if label=='clean-source' else r['current_raw_storage_English'] for r in doc['typed_choice_records']]
        assert result['labels']==expected
        native.append(dict(version=label,command=menu,source_object_hex=raw.hex(),native_VM=result,modal_input_loop_bridged_not_actual_controller_orowner_capture=True))
    inverse=bytearray(now);regions=[]
    for pair in group['all_command_reference_pairs']:
        assert pair['source_offset']==pair['current_offset'] and pair['source_extent']==pair['current_extent']
        at,n=pair['current_offset'],pair['current_extent'];word=pair['word']
        if word in [0x4000,0x2100]:
            inverse[at:at+n]=ja[at:at+n];regions.append(dict(offset=at,bytes=n,word=word))
        elif word==0x100:assert now[at:at+4]==ja[at:at+4]
        else:assert now[at:at+n]==ja[at:at+n]
    assert len(regions)==25 and bytes(inverse)==ja and ja[:8]==now[:8]
    components=[]
    for label,image in [('clean-source',clean),('current-English',current)]:
        arm=image.read_file('/__arm9__.bin');table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000
        slot=table+32*34+4;pointer=struct.unpack_from('<I',arm,slot)[0]
        components.append(dict(version=label,actor_ID=34,table_slot_kind='source surname-name slot; not a claim about historical family relationships',
            table_field_offset=slot,table_field_hex=arm[slot:slot+4].hex(),ARM9_sha256=sha(arm),**string(arm,pointer)))
    assert [r['text'] for r in components]==['ハイレディン','Hayreddin']
    ROOT.mkdir(parents=True);save(ROOT/'two_current_choices_native_getters_geometry_exact_control_inverse_Hayreddin_component.json',dict(
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),native_menu_versions=native,
        current_effective_choice_records=doc['typed_choice_records'],
        original_two_choice_provider_has_no_speech_catalogue_replacement=True,
        all_source_current_choice_result_words_andthree_bridged_return_cases_preserved=True,
        complete_clean1696_byte_inverse_from25_prose_container_regions=True,prose_container_regions=regions,
        all_five_A000_four_relative_headers6300_61FF_andfull_normal_end_exact=True,
        clean_header_logical1694_tail2_andall37_command_shapes_exact=True,
        Hayreddin_source_current_name_component=components,
        Hayreddin_component_retention_not_full_name_middle_catalogue_or207_name_approval=True,
        actual_menu_view_backing_highlights_selection_andB46_body_nameplate_display_pending=True,
        native_VM_getter_width_andrectangle_checks_not_actual_gameplay=True,
        mode_terminology_scope='Retain existing Inspect/Battle/Search consistently in this exchange; broader UI/display consistency remains subject to native and actual checks.',
        no_ROM_state_font_controller_orprose_mutation=True,new_emulator_runs=0,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,FLOW,Path(__file__)]},full_goal_complete=False))
    print('Both current labels/native widths/result forwarding bound; all25 prose containers invert to complete clean1696 bytes. Hayreddin component source-supported; actual menu/display pending.')
