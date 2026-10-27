"""Bind complete clean/current B166 commands and canonical typed-label identities after clean glosses."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.map_lil_B122_B127_source_v3260c import choice_getters
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_source_v4054')
PRIOR=Path('work/analysis/editorial_handoff_verification_v4051/verified_handoff.json')
HISTORY=Path('work/analysis/lil_B165_source_v4008/all24_clean_current_complete_context.json')
CLEAN=Path('work/analysis/lil_B166_clean_v4052/complete_clean42_speeches_two_choice_labels_before_English.json')
GLOSS=Path('work/analysis/lil_B166_clean_context_v4053/all44_complete_B166_exchange_and_fresh_glosses.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,history,cleanpacket,gloss=map(read,[PRIOR,HISTORY,CLEAN,GLOSS])
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);assert sha(lp.read_bytes())==prior['ledger_sha256']
    known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']};assert len(known)==5529
    current,clean=NdsImage.open(prior['candidate']),NdsImage.open('work/clean.nds');assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']
    arm,original=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin');spans=[(0x2425C,0x242C8),(0x242CC,0x24310),(0x24314,0x24330),(0x24334,0x243A0),(0x2A1D8,0x2A600)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    source,target=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[166] for im in [clean,current]]
    native,walker,inventory_source=scoped_inventory();old,spoken=native(original,source);now,translated=native(arm,target)
    shape=lambda cs:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in cs]
    assert shape(old)==shape(now) and cleanpacket['block']['clean_block_sha256']==sha(source) and len(old)==62 and len(spoken)==42
    glosses={r['id']:r for r in gloss['records']};rows=[]
    for i,(a,b) in enumerate(zip(spoken,translated,strict=True)):
        sa,ca=a['offset']+5,b['offset']+5;raw=source[sa:source.index(b'\0',sa+1)];value=target[ca:target.index(b'\0',ca+1)]
        assert value[0]==raw[0] in [2,9,20,23] and source[sa-5:sa+1]==target[ca-5:ca+1]
        index=source[:sa].count(b'\0');r=deepcopy(glosses[f'DK4_MES_B166_R{index:04d}']);assert r['source_hex']==raw.hex()
        r.update(current_record_index=target[:ca].count(b'\0'),current_reference=dict(offset=ca,bytes=len(value),header_offset=ca-5),current_hex=value.hex(),source_presentation_prefix_hex=format(raw[0],'02x'),kind='progressive',source_kind='progressive',current_native_extent=b['native_extent'],native_command_extent=a['native_extent'],spoken_sequence_index=i,current_native_voice_macro_entry_and_context_pending=True,source_prose_or_completion_credit_added=0)
        rows.append(r)
    menus=[];choices=[];getters=[];choicegloss={r['source_reference']['offset']:r for r in gloss['typed_choice_records']}
    for a,b in zip(old,now,strict=True):
        if a['word']!=0x2100:continue
        versions=[dict(version=version,command=cmd,alignment_cases=choice_getters(code,cmd)) for version,code,cmd in [('clean',original,a),('current',arm,b)]]
        labels,currentlabels=[v['alignment_cases'][0]['labels'] for v in versions];obj=[]
        for s,t in zip(labels,currentlabels,strict=True):
            option=s['option_index'];assert t['option_index']==option;r=deepcopy(choicegloss[s['offset']]);assert r['source_hex']==s['hex']
            r.update(clean_gloss_precanonical_ID=r['id'],id=f'DK4_CHOICE_B166_C{a["offset"]}_O{option}',command_offset=a['offset'],option_index=option,current_reference=dict(offset=t['offset'],bytes=len(bytes.fromhex(t['hex']))),current_hex=t['hex'],speaker='Player choice about hearing flagship room advice;not recruitment acceptance',current_native_typed_choice_font_reference_and_outcome_binding_pending=True,source_prose_or_completion_credit_added=0)
            choices.append(r);obj.append(r)
        menus.append(dict(command_offset=a['offset'],source_command=a,current_command=b,original_count_and_pointer_cases=versions,records=obj));getters.extend(versions)
    assert len(choices)==2 and len(menus)==1 and menus[0]['command_offset']==2152 and [r['source_Japanese'] for r in choices]==['お願いする','遠慮する']
    assert not known&{historical_key(r) for r in rows+choices} and {r['source_selector'] for r in rows}=={2,9,20,23}
    assert current.read_file('/data/EV2.DK4')==clean.read_file('/data/EV2.DK4') and sha(Path(history['actual_historical_snapshot']).read_bytes())==history['actual_historical_snapshot_sha256']
    macros={k:sum(bytes.fromhex(r['source_hex']).count(k.encode()) for r in rows) for k in ['FI','FA','FO']};assert macros=={'FI':3,'FA':0,'FO':0}
    g=dict(block=166,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),source_header_hex=source[:4].hex(),current_header_hex=target[:4].hex(),all_clean_native_commands=old,all_current_native_commands=now,source_native_commands=old,current_native_commands=now,source_current_native_command_shape_exact=True,records=rows,choices=menus,physical_speeches=42,source_selectors=[2,9,20,23],source_macro_counts=macros,FE_panels=0,relative_sites=8,all_complete_preambles_and_native_command_shapes_equal=True)
    ROOT.mkdir(parents=True)
    save(ROOT/'all44_clean_current_complete_context_with_typed_choice.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC2.DK4',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(arm),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),original_EV2_sha256=sha(current.read_file('/data/EV2.DK4')),actual_historical_snapshot=history['actual_historical_snapshot'],actual_historical_snapshot_sha256=history['actual_historical_snapshot_sha256'],historical_snapshot_ROM=history['historical_snapshot_ROM'],historical_snapshot_is_Lil_London_not_selected_B166=True,blocks=[g],records=rows,typed_choice_records=choices,typed_actor_style_records=[],source_macro_counts=macros,total_editorial_objects=44,speech_objects=42,ordinary_source_speeches=42,system_FE_panels=0,typed_choice_objects=1,typed_choice_labels=2,source_selectors=[2,9,20,23],source_static_actor_selectors=[2,9,20,23],source_native_commands=62,source_relative_sites=8,original_choice_getter_cases=getters,all8_original_label_getters_and4_count_getters_clean_current_even_alignments_pass=True,source_exact_spans=[dict(start=a,end=b,sha256=sha(arm[a:b])) for a,b in spans],source_transcript=cleanpacket['source_transcript'],source_transcript_sha256=cleanpacket['source_transcript_sha256'],whole_exchange_context_notes=str(GLOSS),whole_exchange_context_notes_sha256=sha(GLOSS.read_bytes()),all44_clean_first_glosses_already_recorded_before_current_comparison=True,choice_IDs_reconciled_by_exact_source_offset_and_bytes_without_prose_change=True,current_native_voices_macros_entry_choices_controls_fonts_actual_and_release_pending=True,no_ROM_registry_ledger_orcredit_change=True,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,HISTORY,CLEAN,GLOSS,Path('scripts/map_lil_B122_B127_source_v3260c.py'),Path(__file__)]},full_goal_complete=False))
    print(dict(objects=44,progressive=42,choices=2,commands=62,relative_sites=8,actors=[2,9,20,23],FI=3,credit=0))
