"""Write concise individual decisions from an already bound clean/current packet."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

NAMES={1:'Hodram',4:'Janus Pasar',6:'Julio Erneco',7:'Cristina Erneco',12:'Yukihisa Shiraki',
14:'Emilio Ferog',16:'Gerhard',18:'Charles',24:'Sera',26:'Julian Lopes',41:'Sojin Kurushima',
78:'Sirwood',79:'Mivor Genz',82:'Shopkeeper',95:'Patron',104:'Trader',113:'Port Worker',
147:'Guildmaster',158:'Sailor',162:'Boy',167:'Lady',254:'System (no speaker)'}

def normalize(text):
    return re.sub(r'\b(FI|FA|FO)\b',lambda m:'{MACRO:'+m[1]+'}',text)

def write_packet(current_path,decisions,contexts,out,producer):
    current_path,out,producer=map(Path,[current_path,out,producer])
    assert not out.exists()
    current=load(current_path);rows=[]
    for group in current['groups']:
        block=group['block']
        if block not in decisions:continue
        choices={index:(english,note) for index,english,note in decisions[block]}
        assert len(choices)==len(group['records'])
        for source in group['records']:
            index=source['source_reference']['record_index']
            proposed,note=choices.pop(index);prior=normalize(source['current_comparison_paragraph'])
            english=prior if proposed is None else proposed
            assert english.strip()==english and '\n' not in english and '  ' not in english
            assert not any(token in english for token in ['{LB','{PAD','{ALIGN'])
            assert {key:english.count('{MACRO:'+key+'}') for key in ('FI','FA','FO')}==source['source_macros']
            row={key:source[key] for key in ['id','file_path','block','source_selector','source_hex',
                'source_complete_preamble_hex','source_reference','source_Japanese','source_decode_error',
                'source_0100_ancestors','source_macros','current_hex','current_reference',
                'current_record_index','current_effective_hex','current_catalogue_selected','selected_native_pointer']}
            retained=english==prior
            row.update(source_record_index=index,source_native_extent=source['native_extent'],
                kind='system-FE' if source['source_selector']==254 else 'progressive',
                speaker=NAMES[source['source_selector']],source_meaning=source['source_meaning_gloss'],
                source_meaning_gloss=source['source_meaning_gloss'],context=f'B{block}: '+contexts[block],
                context_reference=f'#/complete_exchange_contexts/{block}',english=english,logical_English=english,
                planned_English_markup='{SPEAKER:'+format(source['source_selector'],'02X')+'}'+english,
                prior_macro_normalized_comparison=prior,
                prior_effective_paragraph_preserved=source['current_comparison_paragraph'],
                current_raw_storage_English=source['current_stored_text'],localization_note=note,finding=note,
                decision='retention' if retained else 'revision',retention_reason=note if retained else None,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                whole_clean_exchange_andcadence_emotional_progression_reviewed=True,
                no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
                formatting_names_glyph_stored_actual_andregistered_release_pending=True)
            rows.append(row)
        assert not choices
    save(out,dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',
        target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=['source','context','localization','naturalness','formatting'],
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],file_path=current['file_path'],
        blocks=list(decisions),complete_exchange_contexts=contexts,records=rows,
        total_editorial_objects=len(rows),physical_speech_objects=len(rows),typed_choice_objects=0,
        revised=sum(r['decision']=='revision' for r in rows),retained=sum(r['decision']=='retention' for r in rows),
        name_bindings='work/analysis/Hodram_B81_B90_new_names_20261101/names.json',
        known_name_reuse='work/analysis/Hodram_B81_B90_new_names_20261101/known_six_reuse.json',
        pending_name_display_finding='Actor14 progressive andfull name contain full-width F;body spelling Ferog is retained withnormal ASCII F. Shared name correction remains pending.',
        current_packet=str(current_path),current_packet_sha256=sha(current_path.read_bytes()),
        ordinary_wrapping_owned_by_formatter=True,all_four_individual_prose_gates_passed=True,
        all_formatting_gates_false=True,new_credit=0,full_goal_complete=False,
        evidence={str(path):sha(path.read_bytes()) for path in [current_path,producer,Path(__file__)]}))
    print(out,len(rows),'decisions',sum(r['decision']=='revision' for r in rows),'revisions',sum(r['decision']=='retention' for r in rows),'retentions;formatting pending.')
