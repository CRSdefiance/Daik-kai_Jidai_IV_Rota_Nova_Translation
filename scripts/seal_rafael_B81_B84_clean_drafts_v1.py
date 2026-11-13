"""Seal325 source-read speech drafts andfive typed player alternatives before old-English extraction."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from translations.rafael_B81_B84_clean_draft_data_v1 import ROWS,CONTEXTS

ROOT=Path('work/analysis/Rafael_B81_B100_clean_20261105')
DATA=Path('translations/rafael_B81_B84_clean_draft_data_v1.py')

if __name__=='__main__':
    target=ROOT/'B81_B84_325_clean_meanings_andlogical_drafts_v1.json';choices_out=ROOT/'B84_five_clean_choice_drafts_v1.json'
    assert not target.exists() and not choices_out.exists()
    pp=ROOT/'clean_source_packet.json';metadata_path=ROOT/'current_name_metadata_andclean_event_context_v1.json'
    packet,metadata,overlap=map(load,[pp,metadata_path,ROOT/'completed_overlap_census_v1.json'])
    assert not overlap['explicit_source_ID_overlap'] and overlap['source_records']==580
    data={}
    for line in ROWS.strip().splitlines():
        b,n,meaning,english=line.split('|',3);key=int(b),int(n);assert key not in data and meaning and english
        assert english.isascii() and '\n' not in english and '  ' not in english
        data[key]=(meaning,english)
    selected=[g for g in packet['groups'] if g['block'] in range(81,85)]
    expected={(g['block'],r['source_reference']['record_index']) for g in selected for r in g['records']}
    assert set(data)==expected and len(data)==325
    names={r['actor_ID']:r['fields'][0]['current_text'] for r in metadata['current_name_metadata']};records=[]
    for g in selected:
        for original in g['records']:
            row=deepcopy(original);key=g['block'],row['source_reference']['record_index'];meaning,english=data[key]
            assert row['source_Japanese'] is not None and not row['source_decode_error']
            assert all(english.count('{MACRO:'+m+'}')==count for m,count in row['source_macros'].items())
            note='Natural complete-exchange draft preserves: '+meaning
            if key in [(83,101),(83,111),(83,226),(83,234),(83,267)]:
                note+=' Familiar sibling-like address is localized without inventing kinship with the rescued child.'
            if key==(82,110):note+=' Heraldo is a provisional source-name rendering, pending a proper-name spelling binding.'
            row.update(source_meaning=meaning,english=english,speaker=names.get(row['source_selector'],'System panel'),
                context=CONTEXTS[g['block']],localization_note=note,
                review=dict(source=True,context=True,localization=False,naturalness=True,formatting=False),
                current_English_comparison_pending=True,native_name_controls_andterm_binding_pending=True,
                source_meaning_anddraft_precede_old_English_comparison=True)
            records.append(row)
    common=dict(translation_policy='natural-dialogue-v2',target_locale='en-US',source_packet=str(pp),source_packet_sha256=sha(pp.read_bytes()),
        metadata_only_exposure=str(metadata_path),metadata_only_exposure_sha256=sha(metadata_path.read_bytes()),
        current_story_English_unconsulted=True,current_name_metadata_consulted_not_native_consumer_approval=True,
        no_new_native_emulation_gameplay_ROM_orcompletion_credit=True,new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [pp,metadata_path,DATA,Path(__file__)]})
    save(target,dict(**common,format='dk4-Rafael-clean-whole-exchange-drafts-v1',records=records,records_count=325,
        complete_exchange_blocks=[81,82,83,84],remaining_packet_speech_drafts=255,
        chapter_order_not_natural_chronology=True,B82_introduction_B81_bullfight_B83_London_return_context_considered=True,
        Gerhard_recruitment_andall_training_paths_source_reviewed=True,all_current_comparisons_native_display_andintegration_pending=True))
    choices=[];g=selected[3];block=bytes.fromhex(g['clean_block_hex'])
    specs={0x2100:([0,24],['ヴェルスを倒しましょう','倒さなくてもいいんです'],
        ['Propose defeating Vels.','Say that Gerhard need not defeat Vels;the ensuing appeal concerns the fleet\'s future,not a claim that Vels is already defeated.'],
        ["Let's defeat Vels.","You don't have to defeat him."]),
        0x2200:([0,20,34],['厳しい訓練を受ける','話だけを聞く','自分のやり方を貫く'],
        ['Choose the tough training.','Choose only to hear the lesson.','Choose to stick to the player\'s own approach.'],
        ["I'll take the tough training.","Just listen to the lesson.","Stick to my own approach."])}
    for c in g['all_source_commands']:
        if c['word'] not in specs:continue
        offsets,japanese,meanings,english=specs[c['word']];raw=bytes.fromhex(c['whole_command_hex']);header=4+2*(len(offsets)-1)
        assert block[c['offset']:c['offset']+len(raw)]==raw and len(raw)==c['native_extent']
        assert list(struct.unpack_from('<'+str(len(offsets)-1)+'H',raw,4))==offsets[1:]
        for i,offset in enumerate(offsets):
            at=header+offset;end=raw.index(0,at);limit=header+offsets[i+1] if i+1<len(offsets) else len(raw)
            value=raw[at:end];assert value.decode('cp932')==japanese[i] and not any(raw[end:limit])
            choices.append(dict(id=f'SC0_B84_NATIVE_CHOICE_{c["offset"]}_{i}',file_path=g['file_path'],block=84,
                kind='typed-choice-label',source_index=i,source_command_offset=c['offset'],source_command_hex=raw.hex(),
                source_relative_label_offset=offset,source_byte_offset=c['offset']+at,source_hex=value.hex(),source_Japanese=japanese[i],
                source_meaning=meanings[i],english=english[i],speaker='Rafael/player choice',context=CONTEXTS[84],
                localization_note='Preserve this selectable intent;consumer geometry andbranch eligibility are not inferred from the text.',
                review=dict(source=True,context=True,localization=False,naturalness=True,formatting=False),
                earlier_English_unconsulted=True,current_English_andnative_caption_review_pending=True,new_credit=0))
    assert len(choices)==5
    save(choices_out,dict(**common,format='dk4-Rafael-clean-typed-choice-drafts-v1',records=choices,records_count=5,
        menus=2,total_speech_andchoice_objects=330,source_offsets_andwhole_commands_exact=True,all_native_caption_geometry_actual_andintegration_pending=True))
    print('Sealed325 clean speech meanings/drafts plus5 player choices acrossfour complete exchanges;255 other packet speech drafts remain. All comparisons/native/display/integration pending;zero credit.')
