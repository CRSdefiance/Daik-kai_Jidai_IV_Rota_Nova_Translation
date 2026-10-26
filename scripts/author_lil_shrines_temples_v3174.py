"""Assemble all235individual clean-source/prose reviews;formatting remains open."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from scripts import lil_priest_cross_sphinx_prose_v3171 as first
from scripts import lil_cult_star_lamp_prose_v3172 as second
from scripts import lil_beans_jar_prose_v3173 as third

ROOT=Path('work/analysis/lil_Shrines_Temples_author_v3174')
COMPARISON=Path('work/analysis/lil_Shrines_Temples_comparison_v3169b/all235_current_effective_comparison_packet.json')
SOURCE=Path('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json')
CONTROL=Path('work/analysis/lil_Shrines_Temples_controls_v3168c/all235_source_current_dispatch_dynamic_styles_and_predicates.json')
CONTEXT=Path('work/analysis/lil_Shrines_Temples_context_v3164b/complete_clean_exchange_context_notes.json')
TERMS=Path('work/analysis/lil_Shrines_Temples_terms_v3170/clean_current_items_cathedral_and_source_roles.json')
VOICES=Path('work/analysis/lil_Shrines_Temples_voices_v3167/current_catalog207_eight_voice_groups_and_dynamic_CF_D0.json')
PATHS={
    'speech':Path('translations/lil_shrines_temples_editorial_manuscript_v1.json'),
    'voice':Path('translations/lil_shrines_temples_actor_style_manuscript_v1.json'),
    'choices':Path('translations/lil_shrines_temples_choice_manuscript_v1.json')}

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists()for p in PATHS.values())
    source,comparison=read(SOURCE),read(COMPARISON);prose={'speech':{},'voice':{},'choices':{}}
    for module in [first,second,third]:
        for kind,field in [('speech','SPEECH'),('voice','VOICE'),('choices','CHOICES')]:
            incoming=getattr(module,field);assert not set(incoming)&set(prose[kind]);prose[kind].update(incoming)
    assert [len(prose[k])for k in ['speech','voice','choices']]==[164,56,15]
    docs={k:[]for k in prose};expected={k:set()for k in prose};speaker={2:'Lil Argot',9:'Camille',16:'Gerhard',20:'Fernando',139:'Priest',151:'Retainer;generic crew voice,not a new noble rank',160:'Villager;source role,not proof of one shared person',177:'Sect Leader',178:'Follower',191:'Donna',207:'Lil Argot;original CF captain provider'}
    for original in comparison['records']:
        row=deepcopy(original);kind='choices'if row['kind']=='typed-choice-label'else'voice'if row['kind']=='typed-4100-actor-style-alternative'else'speech'
        key=(row['block'],row['command_offset'],row['option_index'])if kind=='choices'else(row['block'],row['command_offset'],row['source_reference']['offset']-row['command_offset'])if kind=='voice'else(row['block'],row['source_record_index'])
        expected[kind].add(key);gloss,english,note=prose[kind][key]
        assert all(isinstance(v,str)and v.strip()==v and '\n'not in v and '\r'not in v for v in [gloss,english,note])
        assert all(32<=ord(c)<=126 for c in english) and '{LB'not in english and '{PAD}'not in english and '%'not in english
        raw=bytes.fromhex(row['source_hex'])
        assert all(raw.count(m.encode())==english.count('{MACRO:'+m+'}')for m in ['FI','FA','FO'])
        old=row['current_effective_paragraph']
        for m in ['FI','FA','FO']:old=old.replace(m,'{MACRO:'+m+'}')
        decision='retain-wording'if english==old else'revise'
        if decision=='retain-wording':assert 'retain' in note.lower()
        row.update(source_meaning=gloss,localization_note=note,editorial_decision=decision,
            current_stored_English=row['current_English'],current_English=row['current_effective_macro_template_English'],
            effective_predecessor_paragraph=old,comparison_basis='current original runtime macro template,including exact registered catalog replacements;NFKC presentation forms andcollapsed legacy whitespace',
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            context='Complete clean B'+str(row['block'])+' exchange reviewed in3164b,then all235effective current passages compared after runtime source binding. Preserve conditional branches,style aliases,source religious/cultural context andunearned progress. '+ ' '.join(next(b['whole_exchange_context_notes']for b in read(CONTEXT)['blocks']if b['block']==row['block'])),
            prose_author_module=next(str(Path(m.__file__))for m in [first,second,third]if key in getattr(m,{'speech':'SPEECH','voice':'VOICE','choices':'CHOICES'}[kind])),
            status='source-context-localization-naturalness-reviewed;formatting-native-references-representative-release-pending',
            current_effective_native_dispatch_proof=str(CONTROL),current_macro_native_UI_body_unexecuted=True,editorial_older_English_comparison_pending=False,
            source_prose_or_completion_credit_added=0)
        if kind=='speech':
            prefix=row['source_selector'];row['english']='{SPEAKER:'+f'{prefix:02X}'+'}'+english
            if prefix==254:
                row['speaker']=('Sphinx;unlabeled original FE presenter'if row['block']==105 else'Anonymous Colosseum voice;original FE'if row['block']==109 else'Source narration/inscription/injury notice;original FE'if row['block']==110 else'Anonymous temple voice;original FE')
            else:
                row['kind']='progressive';row['speaker']=speaker[prefix]
            row['original_native_display_consumer']='original_FE5473C_mode1'if prefix==254 else'original_progressive54020'
        elif kind=='voice':
            row['english']='{SPEAKER:D0}'+english;row['speaker']='Original D0 role1 speech provider;source actor-style slots '+str(row['style_indices'])
            row['virtual_formatter_prefix_hex']='d0';row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text']=True
            row['original_native_display_consumer']='original4100_actor_voice_selection_then2425C_progressive54020'
        else:
            row['english']=english;row['speaker']='Player-selected reply/action;no native speaker label';row['original_native_display_consumer']='original2200_three_option_menu;display andVM approval pending'
        if decision=='retain-wording':row['fresh_retained_wording_justification']=note
        docs[kind].append(row)
    assert all(expected[k]==set(prose[k])for k in prose)
    ROOT.mkdir(parents=True);results={}
    evidence={str(p):sha(p.read_bytes())for p in [SOURCE,COMPARISON,CONTROL,CONTEXT,TERMS,VOICES,Path(__file__),*[Path(m.__file__)for m in [first,second,third]]]}
    for kind,path in PATHS.items():
        rows=docs[kind];counts=Counter(r['editorial_decision']for r in rows)
        doc=dict(format='dk4-editorial-source-prose-draft-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path='/data/SC2.DK4',
            current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],source_ROM_sha256=source['source_ROM_sha256'],required_runtime_ARM9_sha256=source['current_ARM9_sha256'],
            source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),control_contract=str(CONTROL),control_contract_sha256=sha(CONTROL.read_bytes()),whole_exchange_context_notes=str(CONTEXT),whole_exchange_context_notes_sha256=sha(CONTEXT.read_bytes()),
            branch_proof='work/analysis/lil_Shrines_Temples_branches_v3160/original_relative_skip_operand_proof.json',item_terminology_reconciliation=str(TERMS),actor_voice_contract=str(VOICES),effective_current_comparison=str(COMPARISON),
            manuscript_kind=kind,records=rows,revised=counts['revise'],retained=counts['retain-wording'],prose_companions={k:str(v)for k,v in PATHS.items()if k!=kind},
            source_4100_eight_style_aliases_and2200_three_answer_order_preserved=True,virtual_D0_markup_must_be_compiled_without_inserting_a_prefix_into_alternative_body=True,
            no_authored_line_breaks_or_padding=True,formatting_review_pending=True,current_native_fonts_three_option_VM_layout_reference_representative_registered_release_pending=True,
            source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,actual_selected_Shrines_Temples_IDs=[],evidence=evidence,full_goal_complete=False)
        save(path,doc);results[kind]=dict(path=str(path),sha256=sha(path.read_bytes()),records=len(rows),revised=counts['revise'],retained=counts['retain-wording'])
    total=Counter(r['editorial_decision']for rows in docs.values()for r in rows)
    save(ROOT/'all235_source_prose_review_receipt.json',dict(manuscripts=results,total_records=235,revised=total['revise'],retained=total['retain-wording'],all235_individual_gloss_context_localization_and_naturalness_reviews_present=True,
        all235_effective_older_English_compared_after_complete_clean_context=True,three_registered_runtime_replacements_not_confused_with_raw_storage=True,all_source_macro_counts_and_speaker_and_alias_metadata_preserved=True,
        formatting_gates_all_false_and_no_native_or_release_approval_inherited=True,evidence=evidence,source_prose_credit_added=0,completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    print(results);print('TOTAL',dict(total),'235source/prose drafts;formatting/native/reference/representative/release pending;zero ledgercredit.')
