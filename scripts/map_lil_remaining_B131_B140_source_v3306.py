"""Fresh clean/current inventory excluding every completed source-location key."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.map_lil_B122_B127_source_v3260c import choice_getters
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_remaining_B131_B140_source_v3306')
PRIOR=Path('work/analysis/editorial_handoff_verification_v3305/verified_handoff.json')
OLD=Path('work/analysis/lil_after_B119_clean_scope_v3257c/complete_clean_next_exchange_inventory.json')
HISTORY=Path('work/analysis/lil_after_London_inventory_v1913/all336_states_and_original_London_town_eligibility.json')
BLOCKS=[131,133,135,136,137,138,139,140]
if __name__=='__main__':
    assert not ROOT.exists();lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);assert sha(lp.read_bytes())==read(PRIOR)['ledger_sha256']
    c=ledger['current_integrated_candidate'];assert c['profile']=='all-routes-unified-v3300' and sha(Path(c['path']).read_bytes())==c['sha256']
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};old=read(OLD);allphysical=[r for b in old['blocks'] for r in b['records']];new=[r for r in allphysical if historical_key(r) not in known]
    assert len(allphysical)==533 and len(new)==255 and sorted({r['block'] for r in new})==BLOCKS and len(allphysical)-len(new)==278
    current,clean=NdsImage.open(c['path']),NdsImage.open('work/clean.nds');arm,original=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin');jp,en=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks for i in [clean,current]]
    history=read(HISTORY);ev=clean.read_file('/data/EV2.DK4');assert current.read_file('/data/EV2.DK4')==ev
    spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x2A1D8,0x2A600)];assert all(arm[a:b]==original[a:b] for a,b in spans)
    inventory,walk,invsource=scoped_inventory();packets=[];rows=[];choices=[];getters=[]
    for n in BLOCKS:
        source,target=jp[n],en[n];commands,speeches=inventory(original,source);now,translated=inventory(arm,target)
        shape=lambda values:[(r['offset'],r['word'],r['native_extent'],r['ancestor_0100_offsets']) for r in values];assert shape(commands)==shape(now)
        records=[];menus=[]
        for sequence,(a,b) in enumerate(zip(speeches,translated,strict=True)):
            sa,ca=a['offset']+5,b['offset']+5;raw=source[sa:source.index(b'\0',sa+1)];value=target[ca:target.index(b'\0',ca+1)];prefix=raw[0]
            assert raw and value and value[0]==prefix and a['native_extent']==(5+len(raw)+2)//2*2 and source[sa-5:sa+1]==target[ca-5:ca+1] and source[sa-5:sa]==bytes.fromhex('0040ffff00')
            ident=f'DK4_MES_B{n}_R{source[:sa].count(bytes([0])):04d}'
            row=dict(id=ident,file_path='/data/SC2.DK4',block=n,source_record_index=source[:sa].count(b'\0'),current_record_index=target[:ca].count(b'\0'),source_reference=dict(offset=sa,bytes=len(raw),header_offset=sa-5),current_reference=dict(offset=ca,bytes=len(value),header_offset=ca-5),source_hex=raw.hex(),current_hex=value.hex(),source_Japanese=raw[1:].decode('cp932'),current_English=value[1:].decode('cp932'),source_complete_preamble_hex=source[sa-5:sa+1].hex(),source_presentation_prefix_hex=format(prefix,'02x'),source_selector=prefix,kind='system-FE' if prefix==254 else 'progressive',speaker='Original FE modal presenter;not actor254' if prefix==254 else 'Source selector'+format(prefix,'02X')+';current identity pending',original_actor_ID=None if prefix==254 else prefix,native_command_extent=a['native_extent'],ancestor_0100_offsets=a['ancestor_0100_offsets'],spoken_sequence_index=sequence,zero_selector_is_real_control_with_nonempty_body=prefix==0,current_macro_dispatch_consumer_and_complete_native_display_pending=True,source_prose_or_completion_credit_added=0)
            assert historical_key(row) not in known;records.append(row);rows.append(row)
        for a,b in zip(commands,now,strict=True):
            assert a['word'] not in [0x2000,0x4100]
            if a['word']!=0x2100:continue
            versions=[dict(version=version,command=command,alignment_cases=choice_getters(code,command)) for version,code,command in [('clean',original,a),('current',arm,b)]]
            sl,tl=[v['alignment_cases'][0]['labels'] for v in versions];obj=[]
            for s,t in zip(sl,tl,strict=True):
                option=s['option_index'];assert t['option_index']==option
                row=dict(id=f'DK4_CHOICE_B{n}_C{a["offset"]}_O{option}',file_path='/data/SC2.DK4',block=n,command_offset=a['offset'],option_index=option,source_reference=dict(offset=s['offset'],bytes=len(bytes.fromhex(s['hex']))),current_reference=dict(offset=t['offset'],bytes=len(bytes.fromhex(t['hex']))),source_hex=s['hex'],current_hex=t['hex'],source_Japanese=s['text'],current_English=t['text'],kind='typed-choice-label',speaker='Player-selected reply;complete exchange context pending',source_prose_or_completion_credit_added=0)
                assert historical_key(row) not in known;choices.append(row);obj.append(row)
            menus.append(dict(command_offset=a['offset'],source_command=a,current_command=b,original_count_and_pointer_cases=versions,records=obj));getters.extend(versions)
        packets.append(dict(block=n,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),all_clean_native_commands=commands,all_current_native_commands=now,source_current_native_command_shape_exact=True,records=records,choices=menus,original_event_source=history['all336_original_events'][n],historical_completion_or_dependency_state_not_current_eligibility=True))
    assert len(rows)==255 and len(choices)==2 and sum(len(b['all_clean_native_commands']) for b in packets)==647 and sum(r['source_selector']==0 for r in rows)==18 and sum(r['kind']=='system-FE' for r in rows)==1
    base=dict(format='dk4-editorial-source-context-packet-v1',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=c['path'],current_ROM_sha256=c['sha256'],current_ARM9_sha256=sha(arm),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(ev),actual_historical_snapshot=history['snapshot'],actual_historical_snapshot_sha256=history['snapshot_sha256'],historical_snapshot_ROM=history['candidate'],historical_snapshot_is_London_not_selected_next_scenes=True,source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],typed_actor_style_records=[],nontext_2000_commands=[],original_choice_getter_cases=getters,all8_original_label_getters_clean_current_even_alignments_pass=True,all_complete_native_preambles_and_nonempty_zero_selector_bodies_preserved=True,whole_clean_context_current_identity_entry_macros_oldEnglish_comparison_and_all_native_release_gates_pending=True,older_English_stored_as_separate_provenance_not_used_as_translation_source=True,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,explicit_unmatched_native_walk=walk,unchanged_inventory_function=invsource,prior_state_inventory=str(HISTORY),prior_state_inventory_sha256=sha(HISTORY.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    ROOT.mkdir(parents=True);full=ROOT/'complete257_remaining_clean_current_context.json';save(full,{**base,'blocks':packets,'records':rows,'typed_choice_records':choices,'total_editorial_objects':257,'speech_objects':255,'ordinary_source_speeches':254,'system_FE_panels':1,'typed_choice_objects':1,'typed_choice_labels':2,'previous533_physical_speeches':533,'completed278_source_location_speeches_excluded':278,'all_completed_B122_B127_B128_B130_B132_B134_and_prior_families_excluded':True,'unique_player_facing_count_still_requires_entry_and_copy_classification':True})
    selected=[b for b in packets if b['block'] in [131,133]];focus=[r for b in selected for r in b['records']];assert len(focus)==61 and sum(len(b['all_clean_native_commands']) for b in selected)==112
    save(ROOT/'next63_B131_B133_clean_current_context.json',{**base,'blocks':selected,'records':focus,'typed_choice_records':choices,'total_editorial_objects':63,'speech_objects':61,'ordinary_source_speeches':60,'system_FE_panels':1,'typed_choice_objects':1,'typed_choice_labels':2,'broader_remaining_packet':str(full),'broader_remaining_packet_sha256':sha(full.read_bytes()),'all18_source00_speeches_require_static_actor_macro_and_route_binding_not_empty_paragraphs':True})
    print('Remaining257 physical source objects:255 speeches/two labels,eight blocks/647commands;278 completed speeches excluded. NextB131/B133:61speech/two labels/112commands,including18 real source00 bodies;zero reviewcredit.')
